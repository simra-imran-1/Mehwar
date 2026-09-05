"""Exact seed-33 policy modules, including the unused critic for identity checks."""

import torch
from torch import nn


def _map_encoder(flattened: int, output: int) -> nn.Sequential:
    return nn.Sequential(
        nn.Sequential(
            nn.Conv2d(8, 16, 3, 1, 1), nn.ReLU(),
            nn.Conv2d(16, 32, 3, 2, 1), nn.ReLU(),
            nn.Conv2d(32, 32, 3, 2, 1), nn.ReLU(), nn.Flatten(),
        ),
        nn.Linear(flattened, output), nn.ReLU(),
    )


class _Features(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.local_encoder = _map_encoder(32 * 3 * 3, 96)
        self.global_encoder = _map_encoder(32 * 8 * 8, 128)
        self.scalar_encoder = nn.Sequential(
            nn.Linear(4, 32), nn.Tanh(), nn.Linear(32, 32), nn.Tanh(),
        )
        self.fusion = nn.Sequential(nn.Linear(256, 256), nn.ReLU())

    def forward(self, observation: dict[str, torch.Tensor]) -> torch.Tensor:
        return self.fusion(torch.cat((
            self.local_encoder(observation["local_map"]),
            self.global_encoder(observation["global_map"]),
            self.scalar_encoder(observation["scalars"]),
        ), dim=1))


class _Mlp(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.policy_net = nn.Sequential(
            nn.Linear(256, 64), nn.Tanh(), nn.Linear(64, 64), nn.Tanh(),
        )
        self.value_net = nn.Sequential(
            nn.Linear(256, 64), nn.Tanh(), nn.Linear(64, 64), nn.Tanh(),
        )


class FrozenPolicy(nn.Module):
    def __init__(self) -> None:
        super().__init__()
        self.features_extractor = _Features()
        # SB3 serializes three aliases of this one shared module.
        self.pi_features_extractor = self.features_extractor
        self.vf_features_extractor = self.features_extractor
        self.mlp_extractor = _Mlp()
        self.action_net = nn.Linear(64, 8)
        self.value_net = nn.Linear(64, 1)

    def forward(self, observation: dict[str, torch.Tensor]) -> torch.Tensor:
        features = self.features_extractor(observation)
        return self.action_net(self.mlp_extractor.policy_net(features))
