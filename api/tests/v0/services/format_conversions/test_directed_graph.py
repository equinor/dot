import json

import pytest

from src.v0.services.classes.arc import Arc
from src.v0.services.classes.decision_tree import DecisionTree
from src.v0.services.classes.influence_diagram import InfluenceDiagram
from src.v0.services.classes.node import DecisionNode
from src.v0.services.format_conversions import arc, directed_graph, node

TESTDATA = "v0/services/testdata"


@pytest.fixture
def influence_diagram(copy_testdata_tmpdir, tmp_path):
    copy_testdata_tmpdir(TESTDATA)
    with open(tmp_path / "used_car_buyer_problem.json") as f:
        data = json.load(f)
    issues = data["vertices"]["issues"]
    issues = [
        {"uuid" if k == "id" else k: v for k, v in issue.items()} for issue in issues
    ]
    data = {
        "nodes": issues,
        "edges": [edge for edge in data["edges"] if edge["label"] == "influences"],
    }
    return data


def test_class_InfluenceDiagramConversion_from_json_fail_no_vertex(caplog):
    as_json = {
        "type": "Junk",
        "name": "C2H5OH",
        "shortname": "veni vidi vici",
        "alternatives": None,
    }
    with pytest.raises(Exception) as exc_info:
        directed_graph.InfluenceDiagramConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == [
        "Data cannot be used to create an InfluenceDiagram: None"
    ]
    assert (
        str(exc_info.value) == "Data cannot be used to create an InfluenceDiagram: None"
    )


def test_class_InfluenceDiagramConversion_from_json_fail_no_id_nodes(caplog):
    as_json = {
        "vertices": [
            {
                "tag": ["State"],
                "type": "junk",
                "shortname": "State",
                "description": "Issue description",
            }
        ]
    }

    with pytest.raises(Exception) as exc_info:
        directed_graph.InfluenceDiagramConversion().from_json(as_json)
    assert "Data cannot be used to create an InfluenceDiagram: None" in [
        r.msg for r in caplog.records
    ]
    assert (
        str(exc_info.value) == "Data cannot be used to create an InfluenceDiagram: None"
    )


def test_class_InfluenceDiagramConversion_from_json_fail_no_focus_decision(caplog):
    as_json = {
        "vertices": [
            {
                "tag": ["State"],
                "type": "Decision",
                "shortname": "State",
                "description": "Issue description",
                "keyUncertainty": "Key",
                "alternatives": ["Peach", "Lemon"],
            }
        ]
    }

    with pytest.raises(Exception) as exc_info:
        directed_graph.InfluenceDiagramConversion().from_json(as_json)
    assert "Data cannot be used to create an InfluenceDiagram: None" in [
        r.msg for r in caplog.records
    ]
    assert (
        str(exc_info.value) == "Data cannot be used to create an InfluenceDiagram: None"
    )


def test_class_InfluenceDiagramConversion_from_json_fail_no_key_uncertainty(caplog):
    as_json = {
        "vertices": [
            {
                "tag": ["State"],
                "type": "Uncertainty",
                "shortname": "State",
                "description": "Issue description",
                "probabilities": {
                    "type": "DiscreteUnconditionalProbability",
                    "probability_function": [[0.8, 0.2]],
                    "variables": {"State": ["Peach", "Lemon"]},
                },
            }
        ]
    }

    with pytest.raises(Exception) as exc_info:
        directed_graph.InfluenceDiagramConversion().from_json(as_json)
    assert "Data cannot be used to create an InfluenceDiagram: None" in [
        r.msg for r in caplog.records
    ]
    assert (
        str(exc_info.value) == "Data cannot be used to create an InfluenceDiagram: None"
    )


def test_class_InfluenceDiagramConversion_from_json_fail_badly_formatted_node(caplog):
    as_json = {
        "nodes": [
            {
                "tag": ["State"],
                "type": "Uncertainty",
                "index": "0",
            }
        ]
    }

    with pytest.raises(Exception) as exc_info:
        directed_graph.InfluenceDiagramConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == [
        "Data cannot be used to create an influence diagram Node: category: None",
        "Data cannot be used to create an InfluenceDiagram: None",
    ]
    assert (
        str(exc_info.value) == "Data cannot be used to create an InfluenceDiagram: None"
    )


def test_DecisionNodeConversion_from_json(influence_diagram):
    result = directed_graph.InfluenceDiagramConversion().from_json(influence_diagram)
    assert isinstance(result, InfluenceDiagram)
    assert result.decision_count == 2
    assert result.uncertainty_count == 2
    assert result.utility_count == 1


def test_DecisionNodeConversion_to_json(influence_diagram):
    diagram = InfluenceDiagram()
    diagram.add_nodes(
        [
            node.InfluenceDiagramNodeConversion().from_json(item)
            for item in influence_diagram["nodes"]
        ]
    )
    diagram.add_arcs(
        [
            arc.ArcConversion().from_json(item, influence_diagram["nodes"])
            for item in influence_diagram["edges"]
        ]
    )
    result = directed_graph.InfluenceDiagramConversion().to_json(diagram)
    assert len(result["nodes"]) == 5
    assert len(result["arcs"]) == 6
    assert result["nodes"][1]["category"] == "Decision"
    assert result["arcs"][1]["label"] == "influences"


def test_DecisionTreeConversion():
    with pytest.raises(NotImplementedError):
        directed_graph.DecisionTreeConversion().from_json(None)

    decision1 = DecisionNode(
        shortname="D1", description="", uuid="11111111-9999-4444-9999-aaaaaaaaaaaa"
    )
    decision2 = DecisionNode(
        shortname="D2", description="", uuid="22222222-9999-4444-9999-bbbbbbbbbbbb"
    )
    dt = DecisionTree()
    dt.add_nodes((decision1, decision2))
    dt.add_arc(Arc(tail=decision1, head=decision2, label="branch"))

    assert directed_graph.DecisionTreeConversion().to_json(dt) == {
        "id": {
            "node_type": "Decision",
            "shortname": "D1",
            "description": "",
            "branch_name": "",
            "alternatives": None,
            "probabilities": None,
            "utility": None,
            "uuid": "11111111-9999-4444-9999-aaaaaaaaaaaa",
        },
        "children": [
            {
                "id": {
                    "node_type": "Decision",
                    "shortname": "D2",
                    "description": "",
                    "branch_name": "branch",
                    "alternatives": None,
                    "probabilities": None,
                    "utility": None,
                    "uuid": "22222222-9999-4444-9999-bbbbbbbbbbbb",
                }
            }
        ],
    }


def test_DecisionTreeConversion_fail_no_root(caplog):
    decision1 = DecisionNode(
        shortname="D1", description="", uuid="11111111-9999-4444-9999-aaaaaaaaaaaa"
    )
    decision2 = DecisionNode(
        shortname="D2", description="", uuid="22222222-9999-4444-9999-bbbbbbbbbbbb"
    )
    dt = DecisionTree()
    dt.add_nodes((decision1, decision2))

    with pytest.raises(Exception) as exc_info:
        directed_graph.DecisionTreeConversion().to_json(dt)
    assert [r.msg for r in caplog.records] == [
        "Decision tree has no defined root node: None"
    ]
    assert str(exc_info.value) == "Decision tree has no defined root node: None"
