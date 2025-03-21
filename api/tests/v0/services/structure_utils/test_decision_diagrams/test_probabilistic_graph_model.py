import pytest

from src.v0.services.structure_utils.decision_diagrams.probabilistic_graph_model import (
    ProbabilisticGraphModelABC,
)


def test_class_ProbabilisticGraphModelABC(monkeypatch):
    monkeypatch.setattr(ProbabilisticGraphModelABC, "__abstractmethods__", set())
    node = ProbabilisticGraphModelABC()
    with pytest.raises(NotImplementedError):
        node.initialize_diagram(None)
    with pytest.raises(NotImplementedError):
        node._to_json_stream()
