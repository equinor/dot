import networkx as nx
import pytest

from src.v0.services.classes.arc import Arc
from src.v0.services.classes.influence_diagram import InfluenceDiagram
from src.v0.services.classes.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
)


@pytest.fixture
def simple_graph():
    n0 = UncertaintyNode(description="Uncertainty node 1", shortname="u1")
    n1 = UncertaintyNode(description="Uncertainty node 2", shortname="u2")
    n2 = UncertaintyNode(description="Uncertainty node 3", shortname="u3")
    n3 = UncertaintyNode(description="Uncertainty node 4", shortname="u4")
    n4 = DecisionNode(description="Decision node 1", shortname="d1")
    n5 = UncertaintyNode(description="Uncertainty node 5", shortname="u5")
    n6 = DecisionNode(description="Decision node 2", shortname="d2")
    n7 = UncertaintyNode(description="Uncertainty node 6", shortname="u6")
    n8 = UncertaintyNode(description="Uncertainty node 7", shortname="u7")
    n9 = UncertaintyNode(description="Uncertainty node 8", shortname="u8")
    n10 = UtilityNode(description="Utility node 1", shortname="v1")

    e0 = Arc(tail=n0, head=n4, label="e0")
    e1 = Arc(tail=n1, head=n4, label="e1")
    e2 = Arc(tail=n2, head=n4, label="e2")
    e3 = Arc(tail=n3, head=n6, label="e3")
    e4 = Arc(tail=n4, head=n6, label="e4")
    e5 = Arc(tail=n4, head=n5, label="e5")
    e6 = Arc(tail=n6, head=n7, label="e6")
    e7 = Arc(tail=n6, head=n8, label="e7")
    e8 = Arc(tail=n6, head=n9, label="e8")
    e9 = Arc(tail=n5, head=n10, label="e9")

    return {
        "nodes": [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10],
        "arcs": [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9]
        }


def graph_to_influence_diagram(graph):
    influence_diagram = InfluenceDiagram()
    influence_diagram.add_nodes(graph["nodes"])
    influence_diagram.add_arcs(graph["arcs"])
    return influence_diagram


def test_class_InfluenceDiagram():
    ID = InfluenceDiagram()
    assert isinstance(ID.graph, nx.DiGraph)


def test_copy():
    ID = InfluenceDiagram()
    assert nx.utils.graphs_equal(ID.graph, ID.copy().graph)



def test_is_acyclic_true(simple_graph):
    ID = InfluenceDiagram()
    ID = graph_to_influence_diagram(simple_graph)
    assert ID.is_acyclic


def test_is_acyclic_false():
    n0 = UncertaintyNode(description="Uncertainty node 1", shortname="u1")
    n1 = UncertaintyNode(description="Uncertainty node 2", shortname="u2")
    n2 = UncertaintyNode(description="Uncertainty node 3", shortname="u3")

    e0 = Arc(tail=n0, head=n1, label="e0")
    e1 = Arc(tail=n1, head=n2, label="e1")

    ID = InfluenceDiagram()
    ID = graph_to_influence_diagram({"nodes": [n0, n1, n2], "arcs": [e0, e1]})
    assert ID.is_acyclic


def test_nodes(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    assert len(ID.nodes) == 11
    assert ID.nodes[0].description == "Uncertainty node 1"


def test_arcs(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    assert len(ID.arcs) == 10
    assert ID.arcs[0].tail.description == "Uncertainty node 1"
    assert ID.arcs[0].label == "e0"


def test_node_uuids(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    result = ID.node_uuids
    assert len(result) == 11
    assert set(result) == {item.uuid for item in simple_graph["nodes"]}


def test_node_in(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    assert ID.node_in(simple_graph["nodes"][0])
    assert not ID.node_in(
        UncertaintyNode(description="Uncertainty node 1", shortname="u1")
        )  # the created node should have a new uuid, so not in the graph


def test_get_parents(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    n4 = simple_graph["nodes"][4]
    result = ID.get_parents(n4)
    target = simple_graph["nodes"][0:3]
    assert result == target


def test_get_parents_fail(caplog, simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    with pytest.raises(Exception) as exc_info:
        ID.get_parents(DecisionNode(description="junk", shortname="D"))
    assert all("The node is not in the graph:" in r.msg for r in caplog.records)
    assert "The node is not in the graph:" in str(exc_info.value)


def test_get_children(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    n6 = simple_graph["nodes"][6]
    result = ID.get_children(n6)
    target = simple_graph["nodes"][7:10]
    assert result == target

    n4 = simple_graph["nodes"][4]
    result = ID.get_children(n4)
    target = [simple_graph["nodes"][5], simple_graph["nodes"][6]]
    assert all(item in target for item in result)
    assert all(item in result for item in target)


def test_get_children_fail(caplog, simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    with pytest.raises(Exception) as exc_info:
        ID.get_children(DecisionNode(description="junk", shortname="D"))
    assert all("The node is not in the graph:" in r.msg for r in caplog.records)
    assert "The node is not in the graph:" in str(exc_info.value)


def test_get_decision_nodes(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    assert ID.get_decision_nodes() == \
        [simple_graph["nodes"][4], simple_graph["nodes"][6]]


def test_get_utility_nodes(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    assert ID.get_utility_nodes() == [simple_graph["nodes"][10]]


def test_get_uncertainty_nodes(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    assert ID.get_uncertainty_nodes() == [
        simple_graph["nodes"][0],
        simple_graph["nodes"][1],
        simple_graph["nodes"][2],
        simple_graph["nodes"][3],
        simple_graph["nodes"][5],
        simple_graph["nodes"][7],
        simple_graph["nodes"][8],
        simple_graph["nodes"][9],
    ]


def test_nodes_count(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    assert ID.decision_count == 2
    assert ID.utility_count == 1
    assert ID.uncertainty_count == 8


def test_has_children(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    n4 = simple_graph["nodes"][4]
    n8 = simple_graph["nodes"][8]
    assert ID.has_children(n4)
    assert not ID.has_children(n8)


def test_get_node_from_uuid(simple_graph):
    ID = graph_to_influence_diagram(simple_graph)
    n4 = simple_graph["nodes"][4]
    uuid = n4.uuid
    node = ID.get_node_from_uuid(uuid)
    assert isinstance(node, DecisionNode)
    assert node.description == "Decision node 1"
    assert node.shortname == "d1"
