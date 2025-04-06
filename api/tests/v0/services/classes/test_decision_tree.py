import networkx as nx
import pytest

from src.v0.services.classes.arc import Arc
from src.v0.services.classes.decision_tree import DecisionTree
from src.v0.services.classes.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
)


@pytest.fixture
def simple_graph():
    n0 = UncertaintyNode(description="Uncertainty node 0", shortname="u0")
    n1 = UncertaintyNode(description="Uncertainty node 1", shortname="u1")
    n2 = UncertaintyNode(description="Uncertainty node 2", shortname="u2")
    n3 = DecisionNode(description="Decision node 0", shortname="d0")
    n4 = DecisionNode(description="Decision node 1", shortname="d1")
    n5 = DecisionNode(description="Decision node 2", shortname="d2")
    n6 = DecisionNode(description="Decision node 3", shortname="d3")
    n7 = DecisionNode(description="Decision node 4", shortname="d4")
    n8 = UtilityNode(description="Utility node 0", shortname="v0")
    n9 = UtilityNode(description="Utility node 1", shortname="v1")
    n10 = UtilityNode(description="Utility node 2", shortname="v2")
    n11 = UtilityNode(description="Utility node 3", shortname="v3")
    n12 = UncertaintyNode(description="Uncertainty node 3", shortname="u3")
    n13 = UtilityNode(description="Utility node 4", shortname="v4")
    n14 = UtilityNode(description="Utility node 5", shortname="v5")
    n15 = UtilityNode(description="Utility node 6", shortname="v6")
    n16 = UtilityNode(description="Utility node 7", shortname="v7")
    n17 = UtilityNode(description="Utility node 8", shortname="v8")
    n18 = UtilityNode(description="Utility node 9", shortname="v9")
    n19 = UtilityNode(description="Utility node 10", shortname="v10")
    n20 = UtilityNode(description="Utility node 11", shortname="v11")
    n21 = UtilityNode(description="Utility node 12", shortname="v12")

    e0 = Arc(tail=n0, head=n1, label="e0")
    e1 = Arc(tail=n1, head=n3, label="e1")
    e2 = Arc(tail=n3, head=n8, label="e2")
    e3 = Arc(tail=n3, head=n9, label="e3")
    e4 = Arc(tail=n1, head=n4, label="e4")
    e5 = Arc(tail=n4, head=n10, label="e5")
    e6 = Arc(tail=n4, head=n11, label="e6")
    e7 = Arc(tail=n4, head=n12, label="e7")
    e8 = Arc(tail=n12, head=n20, label="e8")
    e9 = Arc(tail=n12, head=n21, label="e9")
    e10 = Arc(tail=n0, head=n2, label="e10")
    e11 = Arc(tail=n2, head=n5, label="e11")
    e12 = Arc(tail=n5, head=n13, label="e12")
    e13 = Arc(tail=n5, head=n14, label="e13")
    e14 = Arc(tail=n2, head=n6, label="e14")
    e15 = Arc(tail=n6, head=n15, label="e15")
    e16 = Arc(tail=n6, head=n16, label="e16")
    e17 = Arc(tail=n2, head=n7, label="e17")
    e18 = Arc(tail=n7, head=n17, label="e18")
    e19 = Arc(tail=n7, head=n18, label="e19")
    e20 = Arc(tail=n7, head=n19, label="e20")

    return {
        "nodes": [
            n0,
            n1,
            n2,
            n3,
            n4,
            n5,
            n6,
            n7,
            n8,
            n9,
            n10,
            n11,
            n12,
            n13,
            n14,
            n15,
            n16,
            n17,
            n18,
            n19,
            n20,
            n21,
        ],
        "arcs": [
            e0,
            e1,
            e2,
            e3,
            e4,
            e5,
            e6,
            e7,
            e8,
            e9,
            e10,
            e11,
            e12,
            e13,
            e14,
            e15,
            e16,
            e17,
            e18,
            e19,
            e20,
        ],
    }


def graph_to_decision_tree(graph):
    decision_tree = DecisionTree()
    decision_tree.add_nodes(graph["nodes"])
    decision_tree.add_arcs(graph["arcs"])
    return decision_tree


def test_class_DecisionTree():
    dt = DecisionTree()
    assert isinstance(dt.graph, nx.DiGraph)
    assert dt.root is None
    root = DecisionNode(description="junk", shortname="D")
    dt = DecisionTree(root=root)
    assert len(list(dt.graph)) == 1
    assert dt.root == root


def test_parent(simple_graph):
    dt = DecisionTree()
    dt = graph_to_decision_tree(simple_graph)
    n5 = simple_graph["nodes"][5]
    n2 = simple_graph["nodes"][2]
    assert dt.parent(n5) == n2
