import pytest

from src.v0.services.classes.abstract_probability import ProbabilityABC


def test_class_ProbabilityABC(monkeypatch):
    monkeypatch.setattr(
        ProbabilityABC,
        "__abstractmethods__",
        set(),
    )
    abstract_probability = ProbabilityABC()

    with pytest.raises(NotImplementedError):
        abstract_probability.initialize_nan(None)

    with pytest.raises(NotImplementedError):
        abstract_probability.initialize_uniform(None)

    with pytest.raises(NotImplementedError):
        abstract_probability.variables()

    with pytest.raises(NotImplementedError):
        abstract_probability.get_distribution()
