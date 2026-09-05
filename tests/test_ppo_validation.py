import hashlib
import io
import json
from zipfile import ZipFile

import pytest

from mehwar.controllers import ppo


def test_checksum_rejected_before_zip_or_tensor_loading(tmp_path):
    path = tmp_path / "not-a-checkpoint.zip"
    path.write_bytes(b"untrusted payload")
    with pytest.raises(ValueError, match="SHA256"):
        ppo.MaskablePPOCheckpointAdapter(path)


@pytest.mark.parametrize(
    ("member", "replacement", "message"),
    [("policy.pth", None, "missing"),
     ("data", None, "missing"),
     ("_stable_baselines3_version", None, "missing"),
     ("data", "{", "metadata"),
     ("data", b"\xff", "metadata"),
     ("_stable_baselines3_version", b"\xff", "metadata"),
     ("data", '{"seed": 32, "num_timesteps": 452608}', "seed"),
     ("data", '{"seed": 33, "num_timesteps": 1}', "num_timesteps"),
     ("_stable_baselines3_version", "0.0.0", "version")],
)
def test_archive_metadata_gates(tmp_path, monkeypatch, member, replacement, message):
    members = {
        "policy.pth": b"not deserialized by these metadata tests",
        "data": json.dumps({"seed": 33, "num_timesteps": 452608}),
        "_stable_baselines3_version": "2.9.0",
    }
    if replacement is None:
        del members[member]
    else:
        members[member] = replacement
    path = tmp_path / "synthetic-validation.zip"
    with ZipFile(path, "w") as archive:
        for name, payload in members.items():
            archive.writestr(name, payload)
    # Exercise inner validation independently of the mandatory production hash gate.
    monkeypatch.setattr(ppo, "CHECKPOINT_SHA256",
                        hashlib.sha256(path.read_bytes()).hexdigest())
    with pytest.raises(ValueError, match=message):
        ppo.MaskablePPOCheckpointAdapter(path)


def test_corrupt_zip_rejected_after_checksum_gate(tmp_path, monkeypatch):
    path = tmp_path / "corrupt.zip"
    path.write_bytes(b"PK\x03\x04truncated ZIP archive")
    monkeypatch.setattr(
        ppo, "CHECKPOINT_SHA256", hashlib.sha256(path.read_bytes()).hexdigest(),
    )
    with pytest.raises(ValueError, match="archive metadata"):
        ppo.MaskablePPOCheckpointAdapter(path)


@pytest.fixture
def synthetic_policy_state():
    """Exercise architecture validation without loading or altering real evidence."""
    torch = pytest.importorskip("torch", reason="Actor tests require the ppo extra")
    from mehwar.controllers._frozen_policy import FrozenPolicy

    with torch.random.fork_rng(devices=[]):
        return FrozenPolicy().state_dict()


@pytest.fixture
def checkpoint_for_state(tmp_path, monkeypatch):
    def write_checkpoint(state):
        torch = pytest.importorskip("torch", reason="Actor tests require the ppo extra")
        weights = io.BytesIO()
        torch.save(state, weights)
        path = tmp_path / "synthetic-architecture.zip"
        with ZipFile(path, "w") as archive:
            archive.writestr("policy.pth", weights.getvalue())
            archive.writestr("data", json.dumps({"seed": 33, "num_timesteps": 452608}))
            archive.writestr("_stable_baselines3_version", "2.9.0")
        monkeypatch.setattr(
            ppo, "CHECKPOINT_SHA256", hashlib.sha256(path.read_bytes()).hexdigest(),
        )
        return path

    return write_checkpoint


@pytest.mark.parametrize("prefix", ["pi_", "vf_"])
@pytest.mark.parametrize("mismatch", ["missing", "different"])
def test_feature_aliases_must_exist_and_agree(
    synthetic_policy_state, checkpoint_for_state, prefix, mismatch,
):
    state = synthetic_policy_state
    name = prefix + "features_extractor.fusion.0.bias"
    if mismatch == "missing":
        del state[name]
    else:
        # Replace only this alias; in-place mutation would change all shared aliases.
        state[name] = state[name].clone() + 1
    with pytest.raises(ValueError, match="feature aliases disagree"):
        ppo.MaskablePPOCheckpointAdapter(checkpoint_for_state(state))


@pytest.mark.parametrize(
    ("mismatch", "message"),
    [("missing", "Missing key"), ("unexpected", "Unexpected key"),
     ("shape", "size mismatch")],
)
def test_policy_architecture_is_strict(
    synthetic_policy_state, checkpoint_for_state, mismatch, message,
):
    state = synthetic_policy_state
    if mismatch == "missing":
        del state["action_net.bias"]
    elif mismatch == "unexpected":
        state["unexpected.weight"] = state["action_net.bias"].clone()
    else:
        state["action_net.weight"] = state["action_net.weight"][:7].clone()
    with pytest.raises(RuntimeError, match=message):
        ppo.MaskablePPOCheckpointAdapter(checkpoint_for_state(state))


def test_loading_preserves_caller_rng_and_checkpoint(
    synthetic_policy_state, checkpoint_for_state,
):
    torch = pytest.importorskip("torch", reason="Actor tests require the ppo extra")
    path = checkpoint_for_state(synthetic_policy_state)
    before_bytes = path.read_bytes()
    before_stat = path.stat()
    before_rng = torch.random.get_rng_state().clone()

    adapter = ppo.MaskablePPOCheckpointAdapter(path)
    adapter.reset()

    assert torch.equal(torch.random.get_rng_state(), before_rng)
    assert path.read_bytes() == before_bytes
    assert path.stat().st_size == before_stat.st_size
    assert path.stat().st_mtime_ns == before_stat.st_mtime_ns
