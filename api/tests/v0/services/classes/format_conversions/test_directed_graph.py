import json

import pytest

from src.v0.services.classes.format_conversions import arc, directed_graph, node
from src.v0.services.classes.influence_diagram import InfluenceDiagram

TESTDATA = "v0/services/testdata"


@pytest.fixture
def influence_diagram(copy_testdata_tmpdir, tmp_path):
    copy_testdata_tmpdir(TESTDATA)
    with open(tmp_path / "used_car_buyer_problem.json") as f:
        data = json.load(f)
    issues = data["vertices"]["issues"]
    issues = [
        {"uuid" if k == "id" else k:v for k,v in issue.items()} for issue in issues
        ]
    data = {
        "nodes": issues,
        "arcs": [edge for edge in data["edges"] if edge["label"] == "influences"]
        }
    return data


def test_class_InfluenceDiagramConversion_from_json_fail_no_vertex(caplog):
    as_json = {
        "type": "Junk",
        "name": "C2H5OH",
        "shortname": "veni vidi vici",
        "alternatives" : None
        }
    with pytest.raises(Exception) as exc_info:
        directed_graph.InfluenceDiagramConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == \
        ["Data cannot be used to create an InfluenceDiagram: None"]
    assert str(exc_info.value) == \
        "Data cannot be used to create an InfluenceDiagram: None"


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
    assert "Data cannot be used to create an InfluenceDiagram: None" in \
        [r.msg for r in caplog.records]
    assert str(exc_info.value) == \
        "Data cannot be used to create an InfluenceDiagram: None"


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
    assert "Data cannot be used to create an InfluenceDiagram: None" in \
        [r.msg for r in caplog.records]
    assert str(exc_info.value) == \
        "Data cannot be used to create an InfluenceDiagram: None"


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
                    "variables": {"State": ["Peach", "Lemon"]}
                }
            }
        ]
    }

    with pytest.raises(Exception) as exc_info:
        directed_graph.InfluenceDiagramConversion().from_json(as_json)
    assert "Data cannot be used to create an InfluenceDiagram: None" in \
        [r.msg for r in caplog.records]
    assert str(exc_info.value) == \
        "Data cannot be used to create an InfluenceDiagram: None"


def test_class_InfluenceDiagramConversion_from_json_fail_badly_formatted_node(caplog):
    as_json = {
        "nodes": [{"tag": ["State"], "type": "Uncertainty", "index": "0",}]
    }

    with pytest.raises(Exception) as exc_info:
        directed_graph.InfluenceDiagramConversion().from_json(as_json)
    assert [r.msg for r in caplog.records] == [
        'Data cannot be used to create an influence diagram Node: category: None',
        'Data cannot be used to create an InfluenceDiagram: None'
        ]
    assert str(exc_info.value) == \
        "Data cannot be used to create an InfluenceDiagram: None"


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
            node.InfluenceDiagramNodeConversion().from_json(item) \
                for item in influence_diagram["nodes"]
            ]
        )
    diagram.add_arcs([arc.ArcConversion().from_json(
        item, influence_diagram["nodes"]) for item in influence_diagram["arcs"]]
        )
    result = directed_graph.InfluenceDiagramConversion().to_json(diagram)
    assert len(result["nodes"]) == 5
    assert len(result["arcs"]) == 6
    assert result["nodes"][1]["category"] == "Decision"
    assert result["arcs"][1]["label"] == "influences"
