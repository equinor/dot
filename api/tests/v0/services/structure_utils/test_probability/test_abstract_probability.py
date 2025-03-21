import pytest

from src.v0.services.structure_utils.probability.abstract_probability import (
    ProbabilityABC,
)


def test_class_ProbabilityABC(monkeypatch):
    monkeypatch.setattr(
        ProbabilityABC,
        "__abstractmethods__",
        set(),
    )
    abstract_probability = ProbabilityABC()
    with pytest.raises(NotImplementedError):
        ProbabilityABC.from_db_model()

    with pytest.raises(NotImplementedError):
        abstract_probability.initialize_nan()

    with pytest.raises(NotImplementedError):
        abstract_probability.set_to_uniform()

    with pytest.raises(NotImplementedError):
        abstract_probability.normalize()

    with pytest.raises(NotImplementedError):
        abstract_probability.isnormalized()

    with pytest.raises(NotImplementedError):
        abstract_probability.from_json()

    with pytest.raises(NotImplementedError):
        abstract_probability.to_json()

    with pytest.raises(NotImplementedError):
        abstract_probability.to_dict()

    with pytest.raises(NotImplementedError):
        abstract_probability.get_distribution()

    with pytest.raises(NotImplementedError):
        abstract_probability.to_pyagrum()

    with pytest.raises(NotImplementedError):
        abstract_probability.to_pycid()
