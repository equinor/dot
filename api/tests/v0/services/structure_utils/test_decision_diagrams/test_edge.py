import pytest

from src.v0.services.structure_utils.decision_diagrams.edge import Edge
from src.v0.services.structure_utils.decision_diagrams.influence_diagram import (
    InfluenceDiagram,
)
from src.v0.services.structure_utils.decision_diagrams.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
)


def test_class_InformationalArc():
    n1 = UncertaintyNode("J", "junk")
    n2 = DecisionNode("H", "junky")
    edge = Edge(n1, n2, "first")
    assert edge.endpoint_start == n1
    assert edge.endpoint_end == n2
    assert edge.name == "first"
    assert edge._arc_type == "informational"


def test_class_InformationalArc_without_name():
    n1 = UncertaintyNode("J", "junk")
    n2 = DecisionNode("H", "junky")
    edge = Edge(n1, n2)
    assert edge.name is None


def test_class_ConditionalArc():
    n1 = UncertaintyNode("J", "junk")
    n2 = UncertaintyNode("H", "junky")
    edge = Edge(n1, n2, "second")
    assert edge.endpoint_start.description == "junk"
    assert edge.endpoint_start.shortname == "J"
    assert edge.endpoint_end.description == "junky"
    assert edge.endpoint_end.shortname == "H"
    assert edge._name == "second"
    assert edge._arc_type == "conditional"


def test_class_FunctionalArc():
    n1 = UncertaintyNode("J", "junk")
    n2 = UtilityNode("H", "junky")
    edge = Edge(n1, n2, "first")
    assert edge.endpoint_start == n1
    assert edge.endpoint_end == n2
    assert edge.name == "first"
    assert edge._arc_type == "functional"


def test_copy():
    n1 = UncertaintyNode("J", "junk")
    n2 = DecisionNode("H", "junky")
    edge = Edge(n1, n2, "first")
    copied_edge = edge.copy()
    assert copied_edge.endpoint_start == edge.endpoint_start
    assert copied_edge.endpoint_end == edge.endpoint_end
    assert copied_edge.name == edge.name


def test_set_endpoint_with_mode_end():
    n1 = UncertaintyNode("J", "junk")
    n2 = DecisionNode("H", "junky")
    edge = Edge(n1, None, "first")
    assert edge.endpoint_start == n1
    assert edge.endpoint_end is None
    assert edge._name == "first"
    assert edge._arc_type is None
    edge.set_endpoint(n2)
    assert edge.endpoint_end == n2
    assert edge._arc_type == "informational"


def test_set_endpoint_with_mode_end_failing_for_wrong_mode(caplog):
    n1 = UncertaintyNode("J", "junk")
    n2 = DecisionNode("H", "junky")
    edge = Edge(n1, None, "first")
    with pytest.raises(Exception) as exc_info:
        edge.set_endpoint(n2, mode="junk")
    assert [r.msg for r in caplog.records] == ["endpoint cannot be set to mode junk"]
    assert str(exc_info.value) == "endpoint cannot be set to mode junk"


def test_set_endpoint_with_mode_end_failing_for_wrong_end_node(caplog):
    n1 = UtilityNode("J", "junk")
    n2 = DecisionNode("H", "junky")
    edge = Edge(n1, None, "first")
    with pytest.raises(Exception) as exc_info:
        edge.set_endpoint(n2, mode="end")
    assert [r.msg for r in caplog.records] == [
        "utility node can only have other utility nodes as successor"
    ]
    assert (
        str(exc_info.value)
        == "utility node can only have other utility nodes as successor"
    )


def test_set_endpoint_with_mode_start():
    n1 = UncertaintyNode("J", "junk")
    n2 = DecisionNode("H", "junky")
    edge = Edge(None, n2, "first")
    assert edge.endpoint_start is None
    assert edge.endpoint_end == n2
    assert edge._name == "first"
    assert edge._arc_type == "informational"
    edge.set_endpoint(n1, mode="start")
    assert edge.endpoint_start == n1
    assert edge._arc_type == "informational"


def test_from_dict():
    n1 = UncertaintyNode("J", "junk")
    n2 = DecisionNode("H", "junky")
    ID = InfluenceDiagram.from_dict({"nodes": [n1, n2]})
    edge = {"from": n1.uuid, "to": n2.uuid, "name": "first"}
    edge = Edge.from_dict(edge, ID)
    assert edge.endpoint_start == n1
    assert edge.endpoint_end == n2
    assert edge.name == "first"
    assert edge._arc_type == "informational"
