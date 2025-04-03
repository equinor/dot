import numpy as np
import pytest

from src.v0.services.classes.format_conversions.node import (
    DecisionJSONConversion,
    InfluenceDiagramNodeConversion,
    UncertaintyJSONConversion,
    add_metadata,
)
from src.v0.services.classes.format_conversions.probability import ProbabilityConversion
from src.v0.services.classes.node import DecisionNode, UncertaintyNode, UtilityNode


@pytest.fixture
def node():
    return {
        "description": "testing node",
        "shortname": "Node",
        "boundary": "in",
        "comments": [{
            "author": "Jr.",
            "comment": "Nope"
        }],
        "uuid": "a6ab145e-2ca9-49e2-8c4f-9607688e57a9"
    }


@pytest.fixture
def decision_node(node):
    return node | {
        "category": "Decision",
        "decisionType": "Focus",
        "alternatives": ["yes", "no"]
        }


@pytest.fixture
def uncertainty_node(node):
    return node | {
        "category": "Uncertainty",
        "keyUncertainty": "True",
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.3], [0.7]],
            "variables": {"States": ["s1", "s2"]}
        }
    }


@pytest.fixture
def value_metric_node(node):
    return node | {
        "category": "Value Metric"
        }


def test_add_metadata():
    metadata = add_metadata("1")
    assert metadata["uuid"] == "1"


def test_DecisionJSONConversion(decision_node):
    node = InfluenceDiagramNodeConversion().from_json(decision_node)
    assert DecisionJSONConversion().states(node) == ["yes", "no"]
    assert DecisionJSONConversion().decision_type(node) == "Focus"


def test_UncertaintyJSONConversion(uncertainty_node):
    node = InfluenceDiagramNodeConversion().from_json(uncertainty_node)
    assert UncertaintyJSONConversion().probability(node) == {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.3], [0.7]],
            "variables": {"States": ["s1", "s2"]}
        }
    assert UncertaintyJSONConversion().key_uncertainty(node) == "True"
    assert UncertaintyJSONConversion().source(node) == ""


def test_InfluenceDiagramNodeConversion_from_json_fail_not_id_node_due_to_category(
        caplog
        ):
    as_json = {
            "category": "Junk",
            "boundary": "in",
            "description": "C2H5OH",
            "shortname": "veni vidi vici",
            "consequences" : None
            }
    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramNodeConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == \
        ["Data cannot be used to create an influence diagram Node: category: Junk"]
    assert str(exc_info.value) == \
        "Data cannot be used to create an influence diagram Node: category: Junk"


def test_InfluenceDiagramNodeConversion_from_json_fail_not_id_node_due_to_no_shortname(
        caplog
        ):
    as_json = {
            "category": "Decision",
            "boundary": "in",
            "description": "C2H5OH",
            "consequences" : None
            }
    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramNodeConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == \
        ["Data cannot be used to create an influence diagram Node: shortname: None"]
    assert str(exc_info.value) == \
        "Data cannot be used to create an influence diagram Node: shortname: None"


def test_InfluenceDiagramNodeConversion_from_json_fail_not_focus_decision(caplog):
    as_json = {
            "category": "Decision",
            "boundary": "in",
            "decisionType": "junk",
            "description": "C2H5OH",
            "shortname": "veni vidi vici",
            "consequences" : None
            }
    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramNodeConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == \
        ["Data cannot be used to create an influence diagram Node: decisionType: junk"]
    assert str(exc_info.value) == \
        "Data cannot be used to create an influence diagram Node: decisionType: junk"


def test_InfluenceDiagramNodeConversion_from_json_fail_not_key_uncertainty(caplog):
    as_json = {
            "category": "Uncertainty",
            "boundary": "in",
            "keyUncertainty": "junk",
            "description": "C2H5OH",
            "shortname": "veni vidi vici",
            "consequences" : None
            }
    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramNodeConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == \
        ["Data cannot be used to create an influence diagram Node: keyUncertainty: junk"]
    assert str(exc_info.value) == \
        "Data cannot be used to create an influence diagram Node: keyUncertainty: junk"


def test_InfluenceDiagramNodeConversion_from_json_fail_not_in_on_boundary(caplog):
    as_json = {
            "category": "Uncertainty",
            "boundary": "out",
            "keyUncertainty": "True",
            "description": "C2H5OH",
            "shortname": "veni vidi vici",
            "consequences" : None
            }
    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramNodeConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == \
        ["Data cannot be used to create an influence diagram Node: boundary: out"]
    assert str(exc_info.value) == \
        "Data cannot be used to create an influence diagram Node: boundary: out"


def test_InfluenceDiagramNodeConversion_from_json_decision(decision_node):
    result = InfluenceDiagramNodeConversion().from_json(decision_node)
    assert isinstance(result, DecisionNode)
    assert result.description == "testing node"
    assert result.shortname == "Node"
    assert result.alternatives == ["yes", "no"]


def test_InfluenceDiagramNodeConversion_from_json_uncertainty(uncertainty_node):
    result = InfluenceDiagramNodeConversion().from_json(uncertainty_node)
    assert isinstance(result, UncertaintyNode)
    assert result.description == "testing node"
    assert result.shortname == "Node"
    assert result.probability.outcomes == ('s1', 's2')
    assert result.probability.variables == ('States',)
    np.testing.assert_allclose(
        result.probability.get_distribution(), np.array([0.3, 0.7])
        )


def test_InfluenceDiagramNodeConversion_from_json(value_metric_node):
    result = InfluenceDiagramNodeConversion().from_json(value_metric_node)
    assert isinstance(result, UtilityNode)
    assert result.description == "testing node"
    assert result.shortname == "Node"


def test_InfluenceDiagramNodeConversion_to_json_fail_not_influence_diagram_node(caplog):
    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramNodeConversion().to_json(None)
    assert [r.msg for r in caplog.records] == ["Data is not an InfluenceDiagram Node: <class 'NoneType'>"]
    assert str(exc_info.value) == "Data is not an InfluenceDiagram Node: <class 'NoneType'>"


def test_InfluenceDiagramNodeConversion_to_json_decision(decision_node):
    data = DecisionNode(
        description=decision_node['description'],
        shortname=decision_node['shortname'],
        uuid=decision_node['uuid'],
        alternatives=decision_node['alternatives']
        )
    result = InfluenceDiagramNodeConversion().to_json(data)
    assert result["description"] == "testing node"
    assert result["shortname"] == "Node"
    assert result["uuid"] == data.uuid
    assert result["alternatives"] == ["yes", "no"]


def test_InfluenceDiagramNodeConversion_to_json_uncertainty(uncertainty_node):
    probabilities = ProbabilityConversion().from_json(uncertainty_node['probabilities'])
    data = UncertaintyNode(
        description=uncertainty_node['description'],
        shortname=uncertainty_node['shortname'],
        uuid=uncertainty_node['uuid'],
        probability=probabilities
        )
    result = InfluenceDiagramNodeConversion().to_json(data)
    assert result['description'] == uncertainty_node['description']
    assert result['shortname'] == uncertainty_node['shortname']
    assert result['keyUncertainty'] == "True"
    assert result['uuid'] == data.uuid
    assert result['probabilities'] == uncertainty_node['probabilities']


def test_InfluenceDiagramNodeConversion_to_json_utility(value_metric_node):
    data = UtilityNode(
        description=value_metric_node['description'],
        shortname=value_metric_node['shortname'],
        )
    result = InfluenceDiagramNodeConversion().to_json(data)
    assert result['description'] == value_metric_node['description']
    assert result['shortname'] == value_metric_node['shortname']
    assert result['uuid'] == data.uuid
