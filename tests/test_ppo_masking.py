import pytest

from mehwar.controllers.ppo import MaskablePPOCheckpointAdapter

torch = pytest.importorskip("torch", reason="Actor tests require the ppo extra")


class FixedLogits(torch.nn.Module):
    def forward(self, observation):
        assert not torch.is_grad_enabled()
        return torch.tensor([[0., 2., 99., 2., 0., 0., 0., 0.]])


@pytest.fixture
def adapter():
    instance = MaskablePPOCheckpointAdapter.__new__(MaskablePPOCheckpointAdapter)
    instance._policy = FixedLogits()
    instance.reset()
    return instance


@pytest.fixture
def observation():
    return {"local_map": torch.zeros(8, 11, 11),
            "global_map": torch.zeros(8, 32, 32), "scalars": torch.zeros(4)}


def test_mask_excludes_maximum_and_ties_use_lowest_id(adapter, observation):
    assert adapter.act(observation, [3, 1]) == 1
    assert adapter.act(observation, [7]) == 7
    assert adapter.act(observation, list(range(8))) == 2


@pytest.mark.parametrize("actions", [None, [], [-1], [8], [True], [1.0]])
def test_legal_actions_are_required_valid_ids(adapter, observation, actions):
    with pytest.raises(ValueError):
        adapter.act(observation, actions)


def test_bad_observation_shape_and_nonfinite_values(adapter, observation):
    observation["scalars"] = torch.zeros(5)
    with pytest.raises(ValueError, match="scalars"):
        adapter.act(observation, [0])
    observation["scalars"] = torch.full((4,), float("nan"))
    with pytest.raises(ValueError, match="scalars"):
        adapter.act(observation, [0])


def test_duplicate_legal_ids_do_not_change_lowest_id_tie_break(adapter, observation):
    assert adapter.act(observation, [3, 3, 1, 3, 1]) == 1


def test_numpy_integer_legal_ids_return_a_python_integer(adapter, observation):
    numpy = pytest.importorskip("numpy", reason="NumPy actions require the ppo extra")
    action = adapter.act(observation, [numpy.int64(3), numpy.int32(1)])
    assert type(action) is int
    assert action == 1


@pytest.mark.parametrize("value", [float("nan"), float("inf"), -float("inf")])
def test_nonfinite_logits_are_rejected_even_for_a_masked_action(
    adapter, observation, value,
):
    class NonfiniteLogits(torch.nn.Module):
        def forward(self, observation):
            return torch.tensor([[0., 2., value, 2., 0., 0., 0., 0.]])

    adapter._policy = NonfiniteLogits()
    with pytest.raises(ValueError, match="Non-finite frozen actor logits"):
        adapter.act(observation, [1, 3])
