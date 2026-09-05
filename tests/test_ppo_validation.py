import hashlib
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
     ("data", "{", "metadata"),
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
