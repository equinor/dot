from copy import deepcopy

import pytest

from src.v0.services.classes.format_conversions.node import DecisionNodeConversion
from src.v0.services.classes.node import DecisionNode


@pytest.fixture
def decision_node():
    return {
        "description": "testing node",
        "shortname": "Node",
        "boundary": "in",
        "comments": [{"author": "Jr.", "comment": "Nope"}],
        "category": "Decision",
        "decisionType": "Focus",
        "alternatives": ["yes", "no"],
        "uuid": "a6ab145e-2ca9-49e2-8c4f-9607688e57a9",
    }


def test_class_DecisionNodeConversion_from_json_fail(caplog):
    as_json = {
        "category": "Junk",
        "description": "C2H5OH",
        "shortname": "veni vidi vici",
        "alternatives": None,
    }
    with pytest.raises(Exception) as exc_info:
        DecisionNodeConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == [
        "Data cannot be used to create a DecisionNode: Junk"
    ]
    assert str(exc_info.value) == "Data cannot be used to create a DecisionNode: Junk"


def test_DecisionNodeConversion_from_json(decision_node):
    result = DecisionNodeConversion().from_json(decision_node)
    assert isinstance(result, DecisionNode)
    assert result.description == "testing node"
    assert result.shortname == "Node"
    assert result.uuid == "a6ab145e-2ca9-49e2-8c4f-9607688e57a9"
    assert result.alternatives == ["yes", "no"]


def test_DecisionNodeConversion_from_json_no_alternatives(decision_node):
    local_node = deepcopy(decision_node)
    local_node["alternatives"] = None
    result = DecisionNodeConversion().from_json(local_node)
    assert isinstance(result, DecisionNode)
    assert result.description == "testing node"
    assert result.shortname == "Node"
    assert result.alternatives == []


def test_DecisionNodeConversion_to_json(decision_node):
    data = DecisionNode(
        description=decision_node["description"],
        shortname=decision_node["shortname"],
        alternatives=decision_node["alternatives"],
    )
    result = DecisionNodeConversion().to_json(data)
    assert result["description"] == decision_node["description"]
    assert result["shortname"] == decision_node["shortname"]
    assert result["decisionType"] == "Focus"
    assert result["uuid"] == data.uuid
    assert result["alternatives"] == decision_node["alternatives"]


def test_DecisionNodeConversion_to_json_no_alternatives(decision_node):
    data = DecisionNode(
        description=decision_node["description"], shortname=decision_node["shortname"]
    )
    result = DecisionNodeConversion().to_json(data)
    assert result["shortname"] == decision_node["shortname"]
    assert result["description"] == decision_node["description"]
    assert result["decisionType"] == "Focus"
    assert result["uuid"] == data.uuid
    assert result["alternatives"] is None
