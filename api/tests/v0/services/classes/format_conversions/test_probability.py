import numpy as np
import pytest

from src.v0.services.classes.discrete_conditional_probability import (
    DiscreteConditionalProbability as DiscreteConditionalProbability,
)
from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability as DiscreteUnconditionalProbability,
)
from src.v0.services.classes.format_conversions.probability import (
    DiscreteConditionalProbabilityConversion,
    DiscreteUnconditionalProbabilityConversion,
    ProbabilityConversion,
)


def test_class_ProbabilityConversion_from_json_fail_not_dict(caplog):
    with pytest.raises(Exception) as exc_info:
        ProbabilityConversion().from_json("None")
    assert [r.msg for r in caplog.records] == ["Unreckonized probability type: None"]
    assert str(exc_info.value) == "Unreckonized probability type: None"


def test_class_ProbabilityConversion_from_json_fail_wrong_probability(caplog):
    with pytest.raises(Exception) as exc_info:
        ProbabilityConversion().from_json({"type": "unknown"})
    assert [r.msg for r in caplog.records] == [
        "Unreckonized probability type: {'type': 'unknown'}"
    ]
    assert str(exc_info.value) == "Unreckonized probability type: {'type': 'unknown'}"


def test_class_ProbabilityConversion_from_json_conditional():
    as_json = {
        "dtype": "DiscreteConditionalProbability",
        "probability_function": [[0.4, 0.5], [0.6, 0.5]],
        "variables": {
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
        "attributes": {
            "conditioned_variables": ["Node1"],
            "conditioning_variables": ["Node2"],
        },
    }
    result = ProbabilityConversion().from_json(as_json)
    assert isinstance(result, DiscreteConditionalProbability)
    assert result._cpt.attrs == {
        "conditioned_variables": ["Node1"],
        "conditioning_variables": ["Node2"],
    }
    assert result._cpt.coords.dims == ("Node1", "Node2")
    assert result._cpt.coords["Node1"].values.tolist() == ["Outcome1", "Outcome2"]
    assert result._cpt.coords["Node2"].values.tolist() == ["Outcome21", "Outcome22"]
    assert result._cpt.data.tolist() == [[0.4, 0.5], [0.6, 0.5]]


def test_class_ProbabilityConversion_from_json_unconditional():
    as_json = {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[0.2, 0.4], [0.1, 0.3]],
        "variables": {
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
        "attributes": {
            "conditioned_variables": ["Node1"],
            "conditioning_variables": ["Node2"],
        },
    }
    result = ProbabilityConversion().from_json(as_json)
    assert isinstance(result, DiscreteUnconditionalProbability)
    assert result._cpt.attrs == {}
    assert result._cpt.coords.dims == ("Node1", "Node2")
    assert result._cpt.coords["Node1"].values.tolist() == ["Outcome1", "Outcome2"]
    assert result._cpt.coords["Node2"].values.tolist() == ["Outcome21", "Outcome22"]
    assert result._cpt.data.tolist() == [[0.2, 0.4], [0.1, 0.3]]


def test_class_ProbabilityConversion_to_json_conditional():
    values = np.array([[0.1, 0.7, 0.6], [0.9, 0.3, 0.4]])
    conditioned_variable = {"A": ["yes", "no"]}
    conditioning_variable = {"B": ["low", "mid", "high"]}
    variables = conditioned_variable | conditioning_variable
    cpt = DiscreteConditionalProbability(values, variables)
    result = ProbabilityConversion().to_json(cpt)

    target = {
        "dtype": "DiscreteConditionalProbability",
        "probability_function": [[0.1, 0.7, 0.6], [0.9, 0.3, 0.4]],
        "variables": {"A": ["yes", "no"], "B": ["low", "mid", "high"]},
    }
    assert result == target


def test_class_ProbabilityConversion_to_json_unconditional():
    values = np.array([[0.2, 0.4], [0.1, 0.3]])
    variables = {"A": ["yes", "no"], "B": ["low", "high"]}
    cpt = DiscreteUnconditionalProbability(values, variables)
    result = ProbabilityConversion().to_json(cpt)

    target = {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[0.2, 0.4], [0.1, 0.3]],
        "variables": {"A": ["yes", "no"], "B": ["low", "high"]},
    }
    assert result == target


def test_class_DiscreteConditionalProbabilityConversion_from_json_fail(caplog):
    as_json = {
        "dtype": "Junk",
        "probability_function": [[0.4, 0.5], [0.6, 0.5]],
        "variables": {
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
        "attributes": {
            "conditioned_variables": ["Node1"],
            "conditioning_variables": ["Node2"],
        },
    }
    with pytest.raises(Exception) as exc_info:
        DiscreteConditionalProbabilityConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == [
        "Data cannot be used to create a DiscreteConditionalProbability: Junk"
    ]
    assert (
        str(exc_info.value)
        == "Data cannot be used to create a DiscreteConditionalProbability: Junk"
    )


def test_class_DiscreteConditionalProbabilityConversion_from_json():
    as_json = {
        "dtype": "DiscreteConditionalProbability",
        "probability_function": [[0.4, 0.5], [0.6, 0.5]],
        "variables": {
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
        "attributes": {
            "conditioned_variables": ["Node1"],
            "conditioning_variables": ["Node2"],
        },
    }
    result = DiscreteConditionalProbabilityConversion().from_json(as_json)
    assert isinstance(result, DiscreteConditionalProbability)
    assert result._cpt.attrs == {
        "conditioned_variables": ["Node1"],
        "conditioning_variables": ["Node2"],
    }
    assert result._cpt.coords.dims == ("Node1", "Node2")
    assert result._cpt.coords["Node1"].values.tolist() == ["Outcome1", "Outcome2"]
    assert result._cpt.coords["Node2"].values.tolist() == ["Outcome21", "Outcome22"]
    assert result._cpt.data.tolist() == [[0.4, 0.5], [0.6, 0.5]]


def test_class_DiscreteConditionalProbabilityConversion_to_json():
    values = np.array([[0.1, 0.7, 0.6], [0.9, 0.3, 0.4]])
    conditioned_variable = {"A": ["yes", "no"]}
    conditioning_variable = {"B": ["low", "mid", "high"]}
    variables = conditioned_variable | conditioning_variable
    cpt = DiscreteConditionalProbability(values, variables)
    result = DiscreteConditionalProbabilityConversion().to_json(cpt)

    target = {
        "dtype": "DiscreteConditionalProbability",
        "probability_function": [[0.1, 0.7, 0.6], [0.9, 0.3, 0.4]],
        "variables": {"A": ["yes", "no"], "B": ["low", "mid", "high"]},
    }
    assert result == target


def test_class_DiscreteUnconditionalProbabilityConversion_from_json_fail(caplog):
    as_json = {
        "dtype": "Junk",
        "probability_function": [[0.4, 0.5], [0.6, 0.5]],
        "variables": {
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
        "attributes": {
            "conditioned_variables": ["Node1"],
            "conditioning_variables": ["Node2"],
        },
    }
    with pytest.raises(Exception) as exc_info:
        DiscreteUnconditionalProbabilityConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == [
        "Data cannot be used to create a DiscreteUnconditionalProbability: Junk"
    ]
    assert (
        str(exc_info.value)
        == "Data cannot be used to create a DiscreteUnconditionalProbability: Junk"
    )


def test_class_DiscreteUnconditionalProbabilityConversion_from_json():
    as_json = {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[0.2, 0.4], [0.1, 0.3]],
        "variables": {
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
        "attributes": {
            "conditioned_variables": ["Node1"],
            "conditioning_variables": ["Node2"],
        },
    }
    result = DiscreteUnconditionalProbabilityConversion().from_json(as_json)
    assert isinstance(result, DiscreteUnconditionalProbability)
    assert result._cpt.attrs == {}
    assert result._cpt.coords.dims == ("Node1", "Node2")
    assert result._cpt.coords["Node1"].values.tolist() == ["Outcome1", "Outcome2"]
    assert result._cpt.coords["Node2"].values.tolist() == ["Outcome21", "Outcome22"]
    assert result._cpt.data.tolist() == [[0.2, 0.4], [0.1, 0.3]]


def test_class_DiscreteUnconditionalProbabilityConversion_to_json():
    values = np.array([[0.2, 0.4], [0.1, 0.3]])
    variables = {"A": ["yes", "no"], "B": ["low", "high"]}
    cpt = DiscreteUnconditionalProbability(values, variables)
    result = DiscreteUnconditionalProbabilityConversion().to_json(cpt)

    target = {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[0.2, 0.4], [0.1, 0.3]],
        "variables": {"A": ["yes", "no"], "B": ["low", "high"]},
    }
    assert result == target
