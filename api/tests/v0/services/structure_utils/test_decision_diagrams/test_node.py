from unittest.mock import patch

import pytest

from src.v0.models.issue import IssueResponse
from src.v0.services.structure_utils.decision_diagrams.node import (
    DecisionNode,
    NodeABC,
    UncertaintyNode,
    UtilityNode,
)
from src.v0.services.structure_utils.probability.discrete_unconditional_probability import (  # noqa: E501
    DiscreteUnconditionalProbability,
)


def test_class_NodeABC(monkeypatch):
    monkeypatch.setattr(NodeABC, "__abstractmethods__", set())
    with pytest.raises(NotImplementedError):
        NodeABC._from_db_model()

    with pytest.raises(NotImplementedError):
        states = NodeABC("J", "J").states  # assignment to variables only for ruff
        assert states


def test_NodeABC(monkeypatch):
    monkeypatch.setattr(NodeABC, "__abstractmethods__", set())
    with pytest.raises(NotImplementedError):
        NodeABC.get_instance_input(None)


def test_class_DecisionNode():
    node = DecisionNode("J", "junk")
    assert node.description == "junk"
    assert node.shortname == "J"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert isinstance(node.alternatives, list) and not node.alternatives
    assert isinstance(node.states, list) and not node.states
    assert node.is_decision_node
    assert not node.is_uncertainty_node
    assert not node.is_utility_node


def test_class_UncertaintyNode():
    node = UncertaintyNode("J", "junk")
    assert node.description == "junk"
    assert node.shortname == "J"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert node.probabilities is None
    assert isinstance(node.outcomes, tuple) and not node.outcomes
    assert isinstance(node.states, tuple) and not node.states
    assert not node.is_decision_node
    assert node.is_uncertainty_node
    assert not node.is_utility_node


def test_class_UtilityNode():
    node = UtilityNode("J", "junk")
    assert node.description == "junk"
    assert node.shortname == "J"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert isinstance(node.utility, list) and not node.utility
    assert isinstance(node.states, list) and not node.states
    assert not node.is_decision_node
    assert not node.is_uncertainty_node
    assert node.is_utility_node


def test_copy():
    node = DecisionNode("J", "junk", alternatives=["a0", "a1", "a2"])
    copied_node = node.copy()
    assert isinstance(copied_node, type(node))
    assert copied_node.description == node.description
    assert copied_node.shortname == node.shortname
    assert copied_node.alternatives == node.alternatives


@patch("src.v0.services.structure_utils.decision_diagrams.node.uuid4")
def test_DecisionNode_to_dict(uuid_mocker):
    uuid_mocker.return_value = "mocked_uuid"
    node = DecisionNode("J", "junk")
    node.__junk = 3.14
    node.junky = "Coke"
    assert node.to_dict() == {
        "node_type": "DecisionNode",
        "description": "junk",
        "shortname": "J",
        "uuid": "mocked_uuid",
        "alternatives": [],
        "junk": None,
        "junky": "Coke",
    }


@patch("src.v0.services.structure_utils.decision_diagrams.node.uuid4")
def test_UncertaintyNode_to_dict(uuid_mocker):
    uuid_mocker.return_value = "mocked_uuid"
    probabilities = DiscreteUnconditionalProbability(
        probability_function=[[0.5, 0.5], [0.4, 0.6]],
        variables={
            "Node1": ["Outcome1", "Outcome2"],
            "Node2": ["Outcome21", "Outcome22"],
        },
    )
    node = UncertaintyNode("J", "junk", probabilities=probabilities)
    assert node.to_dict() == {
        "node_type": "UncertaintyNode",
        "description": "junk",
        "shortname": "J",
        "uuid": "mocked_uuid",
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.5, 0.5], [0.4, 0.6]],
            "variables": {
                "Node1": ["Outcome1", "Outcome2"],
                "Node2": ["Outcome21", "Outcome22"],
            },
        },
    }


@patch("src.v0.services.structure_utils.decision_diagrams.node.uuid4")
def test_UtilityNode_to_dict(uuid_mocker):
    uuid_mocker.return_value = "mocked_uuid"
    node = UtilityNode("J", "junk")
    assert node.to_dict() == {
        "node_type": "UtilityNode",
        "description": "junk",
        "shortname": "J",
        "uuid": "mocked_uuid",
        "utility": [],
    }


def test_from_dict():
    node = {"node_type": "DecisionNode", "description": "junk", "shortname": "J"}
    node = NodeABC.from_dict(node)
    assert node.description == "junk"
    assert node.shortname == "J"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert isinstance(node.alternatives, list) and not node.alternatives
    assert node.is_decision_node
    assert not node.is_uncertainty_node
    assert not node.is_utility_node


def test_from_dict_fail(caplog):
    node = {"node_type": "UnknownNode", "description": "junk", "shortname": "J"}
    with pytest.raises(Exception) as exc_info:
        NodeABC.from_dict(node)
    assert [r.msg for r in caplog.records] == ["failing instantiation of UnknownNode"]
    assert str(exc_info.value) == "failing instantiation of UnknownNode"


def test_from_db_uncertainty_node_2d_unconditional():
    json_object = {
        "tag": ["State"],
        "category": "Uncertainty",
        "index": "0",
        "description": "Joe does not know the state of the car",
        "shortname": "State",
        "keyUncertainty": "true",
        "decisionType": "",
        "alternatives": ["Peach", "Lemon"],
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.5, 0.5], [0.4, 0.6]],
            "variables": {
                "Node1": ["Outcome1", "Outcome2"],
                "Node2": ["Outcome21", "Outcome22"],
            },
        },
        "influenceNodeUUID": "",
        "boundary": "",
        "comments": [{"comment": "", "author": ""}],
        "uuid": "51cd8e4f-aa04-48e2-8cdf-83a3c9ef978e",
        "timestamp": "1712648453.1573343",
        "date": "2024-04-09 07:40:53.157336",
        "ids": "test",
        "id": "51cd8e4f-aa04-48e2-8cdf-83a3c9ef978e",
        "label": "issue",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
    }

    response = IssueResponse(**json_object)
    result = NodeABC.from_db(response)
    assert isinstance(result, UncertaintyNode)
    assert result.description == "Joe does not know the state of the car"
    assert result.shortname == "State"
    assert result.uuid == "51cd8e4f-aa04-48e2-8cdf-83a3c9ef978e"
    assert isinstance(result.probabilities, DiscreteUnconditionalProbability)
    assert result.states == (
        ("Outcome1", "Outcome21"),
        ("Outcome1", "Outcome22"),
        ("Outcome2", "Outcome21"),
        ("Outcome2", "Outcome22"),
    )
    assert (
        result.probabilities.get_distribution(Node1="Outcome1", Node2="Outcome21") == 0.5
    )


def test_from_db_uncertainty_node_1d_unconditional():
    json_object = {
        "tag": ["State"],
        "category": "Uncertainty",
        "index": "0",
        "description": "Joe does not know the state of the car",
        "shortname": "State",
        "keyUncertainty": "true",
        "decisionType": "",
        "alternatives": ["Peach", "Lemon"],
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.6, 0.4]],
            "variables": {"Node1": ["Outcome1", "Outcome2"]},
        },
        "influenceNodeUUID": "",
        "boundary": "",
        "comments": [{"comment": "", "author": ""}],
        "uuid": "51cd8e4f-aa04-48e2-8cdf-83a3c9ef978e",
        "timestamp": "1712648453.1573343",
        "date": "2024-04-09 07:40:53.157336",
        "ids": "test",
        "id": "51cd8e4f-aa04-48e2-8cdf-83a3c9ef978e",
        "label": "issue",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
    }

    response = IssueResponse(**json_object)
    result = NodeABC.from_db(response)
    assert isinstance(result, UncertaintyNode)
    assert result.description == "Joe does not know the state of the car"
    assert result.shortname == "State"
    assert result.uuid == "51cd8e4f-aa04-48e2-8cdf-83a3c9ef978e"
    assert isinstance(result.probabilities, DiscreteUnconditionalProbability)
    assert result.states == ("Outcome1", "Outcome2")
    assert result.probabilities.get_distribution(Node1="Outcome1") == 0.6


def test_from_db_decision_node():
    json_object = {
        "tag": ["Test"],
        "category": "Decision",
        "index": "0",
        "description": "Joe can test the car",
        "shortname": "Test",
        "keyUncertainty": "false",
        "decisionType": "Focus",
        "alternatives": ["Test", "no Test"],
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.6, 0.4]],
            "variables": {"Node1": ["Outcome1", "Outcome2"]},
        },
        "influenceNodeUUID": "",
        "boundary": "",
        "comments": [{"comment": "", "author": ""}],
        "uuid": "ad651f50-22de-4f85-a560-bf5fb2d9f706",
        "timestamp": "1712648468.41026",
        "date": "2024-04-09 07:41:08.410262",
        "ids": "test",
        "id": "ad651f50-22de-4f85-a560-bf5fb2d9f706",
        "label": "issue",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
    }
    response = IssueResponse(**json_object)
    result = NodeABC.from_db(response)
    assert isinstance(result, DecisionNode)
    assert result.description == "Joe can test the car"
    assert result.shortname == "Test"
    assert result.uuid == "ad651f50-22de-4f85-a560-bf5fb2d9f706"
    assert result.states == ["Test", "no Test"]
    assert result.alternatives == ["Test", "no Test"]


def test_from_db_utility_node():
    json_object = {
        "tag": ["Value"],
        "category": "Value Metric",
        "index": "0",
        "description": "Value",
        "shortname": "Value",
        "keyUncertainty": "false",
        "decisionType": "",
        "alternatives": ["Test"],
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.6, 0.4]],
            "variables": {"Node1": ["Outcome1", "Outcome2"]},
        },
        "influenceNodeUUID": "",
        "boundary": "",
        "comments": [{"comment": "", "author": ""}],
        "uuid": "d52cadfd-c3b8-4531-8e3b-b7e966271edb",
        "timestamp": "1712648501.9647892",
        "date": "2024-04-09 07:41:41.964793",
        "ids": "test",
        "id": "d52cadfd-c3b8-4531-8e3b-b7e966271edb",
        "label": "issue",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
    }
    response = IssueResponse(**json_object)
    result = NodeABC.from_db(response)
    assert isinstance(result, UtilityNode)
    assert result.description == "Value"
    assert result.shortname == "Value"
    assert result.uuid == "d52cadfd-c3b8-4531-8e3b-b7e966271edb"


def test_from_db_fail_node_type():
    json_object = {
        "tag": ["Value"],
        "category": "Junky",
        "index": "0",
        "description": "Value",
        "shortname": "Value",
        "keyUncertainty": "false",
        "decisionType": "",
        "alternatives": ["Test"],
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.6, 0.4]],
            "variables": {"Node1": ["Outcome1", "Outcome2"]},
        },
        "influenceNodeUUID": "",
        "boundary": "",
        "comments": [{"comment": "", "author": ""}],
        "uuid": "d52cadfd-c3b8-4531-8e3b-b7e966271edb",
        "timestamp": "1712648501.9647892",
        "date": "2024-04-09 07:41:41.964793",
        "ids": "test",
        "id": "d52cadfd-c3b8-4531-8e3b-b7e966271edb",
        "label": "issue",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
    }
    response = IssueResponse(**json_object)
    with pytest.raises(Exception) as exc:
        NodeABC.from_db(response)
    assert str(exc.value) == "failing instantiation of JunkyNode"
