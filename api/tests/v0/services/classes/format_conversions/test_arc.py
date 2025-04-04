import json
import pytest 

from src.v0.services.classes.format_conversions import arc, node
# from src.v0.services.structure_utils.decision_diagrams.influence_diagram import InfluenceDiagram
from src.v0.services.classes.arc import Arc

# from src.v0.models.edge import EdgeResponse
# from src.v0.models.structure import InfluenceDiagramResponse, DecisionTreeNodeResponse


TESTDATA = "v0/services/testdata"

@pytest.fixture
def influence_diagram(copy_testdata_tmpdir, tmp_path):
    copy_testdata_tmpdir(TESTDATA)
    with open(tmp_path / "simple_id.json") as f:
        data = json.load(f)
    issues = data["vertices"]["issues"]
    issues = [
        {"uuid" if k == "id" else k:v for k,v in issue.items()} for issue in issues
        ]
    data = {
        "issues": issues,
        "edges": [edge for edge in data["edges"] if edge["label"] == "influences"]
        }
    return data


def test_class_ArcConversion_from_json_fail_not_head(caplog):
    as_json = {
        "id": "a6ab145e-2ca9-49e2-8c4f-9607688e57a9",
        "outV": "98e3d193-d830-452f-9fe8-c21d258ef603",
        "inV": "d52cadfd-c3b8-4531-8e3b-b7e966271edb",
        "uuid": "a6ab145e-2ca9-49e2-8c4f-9607688e57a9",
        "label": "influences"
    }
    issues = [
      {
        "description": "Joe does not know the state of the car",
        "uuid": "51cd8e4f-aa04-48e2-8cdf-83a3c9ef978e",
      },]
    with pytest.raises(Exception) as exc_info:
        arc.ArcConversion().from_json(as_json, issues)
    assert [r.msg for r in caplog.records] == \
      ["Data cannot be used to create an Arc: ([], [])"]
    assert str(exc_info.value) == \
      "Data cannot be used to create an Arc: ([], [])"


def test_class_ArcConversion_from_json_fail_not_edge(caplog):
    as_json = {
        "id": "a6ab145e-2ca9-49e2-8c4f-9607688e57a9",
        "uuid": "a6ab145e-2ca9-49e2-8c4f-9607688e57a9",
        "label": "influences"
    }
    issues = [
      {
        "description": "Joe does not know the state of the car",
        "uuid": "51cd8e4f-aa04-48e2-8cdf-83a3c9ef978e",
      },]
    with pytest.raises(Exception) as exc_info:
        arc.ArcConversion().from_json(as_json, issues)
    assert [r.msg for r in caplog.records] == \
      ["Data cannot be used to create an Arc: ['id', 'uuid', 'label']"]
    assert str(exc_info.value) == \
      "Data cannot be used to create an Arc: ['id', 'uuid', 'label']"


def test_class_ArcConversion_from_json(influence_diagram):
    # First "influences" edge is actually b -> v
    result = arc.ArcConversion().from_json(
        influence_diagram['edges'][0],
        influence_diagram['issues']
        )
    assert isinstance(result, Arc)
    assert result.tail.description == "b"
    assert result.head.description == "v"


def test_class_ArcConversion_to_json(influence_diagram):
    # Arc b->v (issues 0 and 2)
    tail = node.InfluenceDiagramNodeConversion().from_json(
        influence_diagram["issues"][0]
        )
    head = node.InfluenceDiagramNodeConversion().from_json(
        influence_diagram["issues"][2]
        )
    edge = Arc(tail=tail, head=head)
    result = arc.ArcConversion().to_json(edge, [tail, head])
    assert result["outV"] == "b1f3d18d-20a8-475b-981f-32449d1ee6bd"
    assert result["inV"] == "8106127e-ab4a-4aa5-a865-8b55789e7d7a"
    assert result["uuid"] == edge.uuid
