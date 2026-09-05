"""Inference-only adapter pinned to the verified external seed-33 SB3 ZIP."""

from __future__ import annotations

import hashlib
import io
import json
from collections.abc import Mapping, Sequence
from numbers import Integral
from pathlib import Path
from zipfile import BadZipFile, ZipFile

from mehwar.contracts import Controller, JsonValue

CHECKPOINT_FILENAME = "model_stage_301056_lifetime_452608.zip"
CHECKPOINT_SHA256 = "c91d30711aa91957554dfa92b152d2a1d1e14a7b43fa01237722c54cb0acfaaf"
CHECKPOINT_SEED = 33
CHECKPOINT_TIMESTEPS = 452608
PARAMETER_COUNT = 428937
SB3_VERSION = "2.9.0"
OBSERVATION_SHAPES = {
    "local_map": (8, 11, 11), "global_map": (8, 32, 32), "scalars": (4,),
}


class MaskablePPOCheckpointAdapter(Controller[Mapping[str, object], int]):
    """Load verified weights on CPU, with no training or checkpoint write path.

    JSON metadata is inspected without executing SB3's cloudpickled objects.
    The parameter count is over unique policy modules, including the critic.
    """

    def __init__(self, checkpoint_path: str | Path) -> None:
        path = Path(checkpoint_path)
        checkpoint = path.read_bytes()
        digest = hashlib.sha256(checkpoint).hexdigest()
        if digest != CHECKPOINT_SHA256:
            raise ValueError("Checkpoint SHA256 does not match frozen seed-33 model")
        try:
            with ZipFile(io.BytesIO(checkpoint)) as archive:
                required = {"policy.pth", "data", "_stable_baselines3_version"}
                if not required.issubset(archive.namelist()):
                    raise ValueError("Checkpoint is missing required SB3 ZIP members")
                data = json.loads(archive.read("data"))
                version = archive.read("_stable_baselines3_version").decode().strip()
                weights = archive.read("policy.pth")
        except (BadZipFile, json.JSONDecodeError, UnicodeDecodeError) as exc:
            raise ValueError("Invalid SB3 checkpoint archive metadata") from exc
        if data.get("seed") != CHECKPOINT_SEED:
            raise ValueError("Checkpoint seed must be 33")
        if data.get("num_timesteps") != CHECKPOINT_TIMESTEPS:
            raise ValueError("Checkpoint num_timesteps must be 452608")
        if version != SB3_VERSION:
            raise ValueError("Checkpoint SB3 version must be 2.9.0")

        import torch

        from mehwar.controllers._frozen_policy import FrozenPolicy

        state = torch.load(io.BytesIO(weights), map_location="cpu", weights_only=True)
        # Confirm aliases agree before strict loading into the shared modules.
        for name, tensor in state.items():
            if name.startswith("features_extractor."):
                for prefix in ("pi_", "vf_"):
                    if prefix + name not in state or not torch.equal(
                        tensor, state[prefix + name]
                    ):
                        raise ValueError("Checkpoint feature aliases disagree")
        # Constructing modules must not alter the caller's random generator state.
        with torch.random.fork_rng(devices=[]):
            self._policy = FrozenPolicy()
        self._policy.load_state_dict(state, strict=True)
        parameter_count = sum(p.numel() for p in self._policy.parameters())
        if parameter_count != PARAMETER_COUNT:
            raise ValueError("Unique policy parameter count must be 428937")
        self._policy.requires_grad_(False)
        self._metadata: dict[str, JsonValue] = {
            "controller_family": "MaskablePPO",
            "checkpoint_filename": path.name,
            "checkpoint_sha256": digest,
            "seed": data["seed"],
            "num_timesteps": data["num_timesteps"],
            "sb3_version": version,
            "parameter_count": parameter_count,
            "parameter_count_scope": "unique full policy modules including critic",
            "deterministic": True,
            "action_masking": True,
            "inference_backend": "direct frozen actor / torch CPU",
            "torch_version": str(torch.__version__),
        }
        self._policy.eval()

    def reset(self, **kwargs: object) -> None:
        """The actor is feed-forward; no recurrent or episode state is retained."""
        self._policy.eval()

    def act(
        self, observation: Mapping[str, object],
        legal_actions: Sequence[int] | None = None,
    ) -> int:
        import torch

        if legal_actions is None or len(legal_actions) == 0:
            raise ValueError("A nonempty legal_actions set is required")
        if any(isinstance(a, bool) or not isinstance(a, Integral) or not 0 <= a < 8
               for a in legal_actions):
            raise ValueError("Legal actions must be integer IDs from 0 through 7")
        # Sorting preserves SB3 argmax's lowest-ID tie break regardless of input order.
        actions = sorted({int(a) for a in legal_actions})
        inputs = {}
        for name, shape in OBSERVATION_SHAPES.items():
            tensor = torch.as_tensor(observation[name], dtype=torch.float32,
                                     device="cpu")
            if tuple(tensor.shape) != shape or not torch.isfinite(tensor).all():
                raise ValueError(f"{name} must be finite and have shape {shape}")
            inputs[name] = tensor.unsqueeze(0)
        with torch.inference_mode():
            logits = self._policy(inputs)[0]
            if not torch.isfinite(logits).all():
                raise ValueError("Non-finite frozen actor logits")
            return actions[int(torch.argmax(logits[actions]).item())]

    def metadata(self) -> Mapping[str, JsonValue]:
        return dict(self._metadata)
