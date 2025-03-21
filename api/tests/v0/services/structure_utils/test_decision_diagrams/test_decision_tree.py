import json
from unittest.mock import mock_open, patch

import networkx as nx
import numpy as np
import pytest

from src.v0.services.structure_utils.decision_diagrams.decision_tree import DecisionTree
from src.v0.services.structure_utils.decision_diagrams.edge import Edge
from src.v0.services.structure_utils.decision_diagrams.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
)


@pytest.fixture
def graph_as_dict():
    n0 = UncertaintyNode("u0", "Uncertainty node 0")
    n1 = UncertaintyNode("u1", "Uncertainty node 1")
    n2 = UncertaintyNode("u2", "Uncertainty node 2")
    n3 = DecisionNode("d0", "Decision node 0")
    n4 = DecisionNode("d1", "Decision node 1")
    n5 = DecisionNode("d2", "Decision node 2")
    n6 = DecisionNode("d3", "Decision node 3")
    n7 = DecisionNode("d4", "Decision node 4")
    n8 = UtilityNode("v0", "Utility node 0")
    n9 = UtilityNode("v1", "Utility node 1")
    n10 = UtilityNode("v2", "Utility node 2")
    n11 = UtilityNode("v3", "Utility node 3")
    n12 = UncertaintyNode("u3", "Uncertainty node 3")
    n13 = UtilityNode("v4", "Utility node 4")
    n14 = UtilityNode("v5", "Utility node 5")
    n15 = UtilityNode("v6", "Utility node 6")
    n16 = UtilityNode("v7", "Utility node 7")
    n17 = UtilityNode("v8", "Utility node 8")
    n18 = UtilityNode("v9", "Utility node 9")
    n19 = UtilityNode("v10", "Utility node 10")
    n20 = UtilityNode("v11", "Utility node 11")
    n21 = UtilityNode("v12", "Utility node 12")

    e0 = Edge(n0, n1, name="e0")
    e1 = Edge(n1, n3, name="e1")
    e2 = Edge(n3, n8, name="e2")
    e3 = Edge(n3, n9, name="e3")
    e4 = Edge(n1, n4, name="e4")
    e5 = Edge(n4, n10, name="e5")
    e6 = Edge(n4, n11, name="e6")
    e7 = Edge(n4, n12, name="e7")
    e8 = Edge(n12, n20, name="e8")
    e9 = Edge(n12, n21, name="e9")
    e10 = Edge(n0, n2, name="e10")
    e11 = Edge(n2, n5, name="e11")
    e12 = Edge(n5, n13, name="e12")
    e13 = Edge(n5, n14, name="e13")
    e14 = Edge(n2, n6, name="e14")
    e15 = Edge(n6, n15, name="e15")
    e16 = Edge(n6, n16, name="e16")
    e17 = Edge(n2, n7, name="e17")
    e18 = Edge(n7, n17, name="e18")
    e19 = Edge(n7, n18, name="e19")
    e20 = Edge(n7, n19, name="e20")

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
        "edges": [
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


def test_from_dict(graph_as_dict):
    dt = DecisionTree.from_dict(graph_as_dict)
    assert isinstance(dt.nx, nx.DiGraph)


def test_class_DecisionTree():
    dt = DecisionTree()
    assert isinstance(dt.nx, nx.DiGraph)


def test_set_root(graph_as_dict):
    dt = DecisionTree()
    root = graph_as_dict["nodes"][0]
    dt.set_root(root)
    assert isinstance(dt.nx, nx.DiGraph)
    assert dt.parent(root) is None
    assert len(dt.get_children(root)) == 0


def test_initialize_decision_tree(graph_as_dict):
    n0 = graph_as_dict["nodes"][0]
    dt = DecisionTree(root=n0)
    assert nx.number_of_nodes(dt.nx) == 1


def test_initialize_decision_tree_fail():
    n0 = UncertaintyNode("u0", "Uncertainty node 0")
    n1 = UncertaintyNode("u1", "Uncertainty node 1")
    n2 = UncertaintyNode("u2", "Uncertainty node 2")
    n3 = DecisionNode("d0", "Decision node 0")
    n4 = DecisionNode("d1", "Decision node 1")
    n5 = DecisionNode("d2", "Decision node 2")

    e0 = Edge(n0, n5, name="e0")
    e1 = Edge(n1, n2, name="e1")
    e2 = Edge(n2, n3, name="e2")
    e3 = Edge(n2, n4, name="e3")

    graph = {
        "nodes": [n0, n1, n2, n3, n4, n5],
        "edges": [e0, e1, e2, e3],
    }

    with pytest.raises(Exception) as exc:
        DecisionTree.initialize_diagram(graph)
    assert str(exc.value) == "Decision tree has no defined root node"


def test_parent(graph_as_dict):
    dt = DecisionTree.from_dict(graph_as_dict)
    n5 = graph_as_dict["nodes"][5]
    n2 = graph_as_dict["nodes"][2]
    assert dt.parent(n5) == n2


def test_to_json(graph_as_dict):
    dt = DecisionTree.from_dict(graph_as_dict)
    result = dt.to_json()
    assert isinstance(json.loads(result), dict)
    assert result.count("description") == 22
    assert result.count("shortname") == 22
    assert result.count("probabilities") == 4
    assert result.count("alternatives") == 5
    assert result.count("utility") == 13
    assert result.count("children") == 9


def test_to_json_with_file(graph_as_dict):
    dt = DecisionTree.from_dict(graph_as_dict)
    with patch("builtins.open", mock_open()) as m:
        dt.to_json("junk")
        m.assert_called_once_with("junk", "w")


def test_to_json_fail_no_root(caplog):
    probabilities = {
        "type": "DiscreteUnconditionalProbability",
        "probability_function": np.array([0.8, 0.2]),
        "variables": {"State": ["Peach", "Lemon"]},
    }
    uncertainty = UncertaintyNode("Symptom", "S", probabilities=probabilities)

    dt = DecisionTree()
    dt.add_node(uncertainty)
    with pytest.raises(Exception) as exc_info:
        dt.to_json()
    assert [r.msg for r in caplog.records] == ["Decision tree has no defined root node"]
    assert str(exc_info.value) == "Decision tree has no defined root node"
