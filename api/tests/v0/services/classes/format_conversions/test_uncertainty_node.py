from copy import deepcopy

import numpy as np
import pytest

from src.v0.services.classes.discrete_conditional_probability import (
    DiscreteConditionalProbability,
)
from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)
from src.v0.services.classes.format_conversions.node import UncertaintyNodeConversion
from src.v0.services.classes.node import UncertaintyNode


@pytest.fixture
def uncertainty_node():
    return {
        "description": "testing node",
        "shortname": "Node",
        "boundary": "in",
        "comments": [{"author": "Jr.", "comment": "Nope"}],
        "category": "Uncertainty",
        "keyUncertainty": "True",
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.3], [0.7]],
            "variables": {"States": ["s1", "s2"]},
        },
        "uuid": "a6ab145e-2ca9-49e2-8c4f-9607688e57a9",
    }


def test_class_UncertaintyNodeConversion_from_json_fail(caplog):
    as_json = {
        "category": "Junk",
        "description": "C2H5OH",
        "shortname": "veni vidi vici",
        "probabilities": None,
    }
    with pytest.raises(Exception) as exc_info:
        UncertaintyNodeConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == [
        "Data cannot be used to create a UncertaintyNode: Junk"
    ]
    assert str(exc_info.value) == "Data cannot be used to create a UncertaintyNode: Junk"


def test_UncertaintyNodeConversion_from_json_no_probability(uncertainty_node):
    local_node = deepcopy(uncertainty_node)
    local_node["probabilities"] = None
    result = UncertaintyNodeConversion().from_json(local_node)
    assert isinstance(result, UncertaintyNode)
    assert result.description == "testing node"
    assert result.shortname == "Node"
    assert result.probability is None


def test_UncertaintyNodeConversion_from_json_unconditional(uncertainty_node):
    result = UncertaintyNodeConversion().from_json(uncertainty_node)
    assert isinstance(result, UncertaintyNode)
    assert result.description == "testing node"
    assert result.shortname == "Node"
    assert result.probability.outcomes == (("s1", "s2"))
    assert result.probability.variables == ("States",)
    np.testing.assert_allclose(
        result.probability.get_distribution(), np.array([0.3, 0.7])
    )


def test_UncertaintyNodeConversion_from_json_conditional(uncertainty_node):
    local_node = deepcopy(uncertainty_node)
    local_node["probabilities"]["dtype"] = "DiscreteConditionalProbability"
    local_node["probabilities"]["probability_function"] = [[0.3, 0.6], [0.7, 0.4]]
    local_node["probabilities"]["variables"] = {"A": ["a1", "a2"], "B": ["b1", "b2"]}
    result = UncertaintyNodeConversion().from_json(local_node)
    assert isinstance(result, UncertaintyNode)
    assert result.description == "testing node"
    assert result.shortname == "Node"
    assert result.probability.outcomes == ("a1", "a2")
    assert result.probability.variables == ("A", "B")
    np.testing.assert_allclose(
        result.probability.get_distribution(), np.array([[0.3, 0.6], [0.7, 0.4]])
    )


def test_UncertaintyNodeConversion_from_json_uncertainty_other(caplog, uncertainty_node):
    local_node = deepcopy(uncertainty_node)
    local_node["probabilities"]["dtype"] = "junk"
    with pytest.raises(Exception) as exc_info:
        UncertaintyNodeConversion().from_json(local_node)
    assert [r.msg for r in caplog.records] == [
        (
            "Unreckonized probability type: "
            "{'dtype': 'junk', "
            "'probability_function': [[0.3], [0.7]], "
            "'variables': {'States': ['s1', 's2']}}"
        ),
        (
            "Data cannot be used to create a UncertaintyNode: "
            ""
            "Unreckonized probability type: "
            "{'dtype': 'junk', "
            "'probability_function': [[0.3], [0.7]], "
            "'variables': {'States': ['s1', 's2']}}"
        ),
    ]
    assert str(exc_info.value) == (
        "Data cannot be used to create a UncertaintyNode: "
        ""
        "Unreckonized probability type: "
        "{'dtype': 'junk', "
        "'probability_function': [[0.3], [0.7]], "
        "'variables': {'States': ['s1', 's2']}}"
    )


def test_UncertaintyNodeConversion_to_json_no_probability(uncertainty_node):
    data = UncertaintyNode(
        description=uncertainty_node["description"],
        shortname=uncertainty_node["shortname"],
    )
    result = UncertaintyNodeConversion().to_json(data)
    assert result["description"] == uncertainty_node["description"]
    assert result["shortname"] == uncertainty_node["shortname"]
    assert result["keyUncertainty"] == "True"
    assert result["uuid"] == data.uuid
    assert result["probabilities"] is None


def test_UncertaintyNodeConversion_to_json_unconditional(uncertainty_node):
    probabilities = DiscreteUnconditionalProbability(
        probability_function=np.array([[0.25, 0.2], [0.25, 0.3]]),
        variables={
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
    )
    data = UncertaintyNode(
        description=uncertainty_node["description"],
        shortname=uncertainty_node["shortname"],
        probability=probabilities,
    )
    result = UncertaintyNodeConversion().to_json(data)
    assert result["description"] == uncertainty_node["description"]
    assert result["shortname"] == uncertainty_node["shortname"]
    assert result["keyUncertainty"] == "True"
    assert result["uuid"] == data.uuid
    assert result["probabilities"] == {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[0.25, 0.2], [0.25, 0.3]],
        "variables": {
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
    }


def test_UncertaintyNodeConversion_to_json_conditional(uncertainty_node):
    probabilities = DiscreteConditionalProbability(
        probability_function=np.array([[0.5, 0.4], [0.5, 0.6]]),
        variables={
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
    )
    data = UncertaintyNode(
        description=uncertainty_node["description"],
        shortname=uncertainty_node["shortname"],
        probability=probabilities,
    )
    result = UncertaintyNodeConversion().to_json(data)
    assert result["description"] == uncertainty_node["description"]
    assert result["shortname"] == uncertainty_node["shortname"]
    assert result["keyUncertainty"] == "True"
    assert result["uuid"] == data.uuid
    assert result["probabilities"]["dtype"] == "DiscreteConditionalProbability"
    assert result["probabilities"]["variables"] == {
        "Node1": ["Outcome1", "Outcome2"],
        "Node2": ["Outcome21", "Outcome22"],
    }
    assert result["probabilities"]["probability_function"] == [[0.5, 0.4], [0.5, 0.6]]


def test_UncertaintyNodeConversion_to_json_uncertainty_other(caplog, uncertainty_node):
    probabilities = DiscreteConditionalProbability(
        probability_function=np.array([[0.5, 0.4], [0.5, 0.6]]),
        variables={
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
    )
    data = UncertaintyNode(
        description=uncertainty_node["description"],
        shortname=uncertainty_node["shortname"],
        probability=probabilities,
    )
    data._probability = "None"
    with pytest.raises(Exception) as exc_info:
        UncertaintyNodeConversion().to_json(data)
    assert [r.msg for r in caplog.records] == [
        "Unreckonized probability type: None",
        (
            "Data cannot be used to create a UncertaintyNode: "
            "Unreckonized probability type: None"
        ),
    ]
    assert str(exc_info.value) == (
        "Data cannot be used to create a UncertaintyNode: "
        "Unreckonized probability type: None"
    )
