import numpy as np
import pytest

from src.v0.services.analysis.id_to_dt import InfluenceDiagramToDecisionTree
from src.v0.services.classes.arc import Arc
from src.v0.services.classes.decision_tree import DecisionTree
from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)
from src.v0.services.classes.influence_diagram import InfluenceDiagram
from src.v0.services.classes.node import DecisionNode, UncertaintyNode, UtilityNode


@pytest.fixture
def influence_diagram():
    n0 = UncertaintyNode(shortname="u1", description="Uncertainty node 1")
    n1 = UncertaintyNode(shortname="u2", description="Uncertainty node 2")
    n2 = UncertaintyNode(shortname="u3", description="Uncertainty node 3")
    n3 = UncertaintyNode(shortname="u4", description="Uncertainty node 4")
    n4 = DecisionNode(shortname="d1", description="Decision node 1")
    n5 = UncertaintyNode(shortname="u5", description="Uncertainty node 5")
    n6 = DecisionNode(shortname="d2", description="Decision node 2")
    n7 = UncertaintyNode(shortname="u6", description="Uncertainty node 6")
    n8 = UncertaintyNode(shortname="u7", description="Uncertainty node 7")
    n9 = UncertaintyNode(shortname="u8", description="Uncertainty node 8")
    n10 = UtilityNode(shortname="v1", description="Utility node 1")

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

    data = {
        "nodes": [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10],
        "arcs": [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9],
    }

    diagram = InfluenceDiagram()
    diagram.add_nodes(data["nodes"])
    diagram.add_arcs(data["arcs"])
    return diagram


def test_decision_elimination_order(influence_diagram):
    result = InfluenceDiagramToDecisionTree().decision_elimination_order(
        influence_diagram
    )
    target = [influence_diagram.nodes[4], influence_diagram.nodes[6]]
    assert all(item in target for item in result)
    assert all(item in result for item in target)


def test_calculate_partial_order(influence_diagram):
    # Test is only reproducing result, not testing logic!
    partial_order = InfluenceDiagramToDecisionTree().calculate_partial_order(
        influence_diagram
    )
    result = [n.shortname for n in partial_order]
    target = ["u1", "u2", "u3", "d1", "u4", "d2", "u5", "u6", "u7", "u8"]
    assert result == target


def test_calculate_partial_order_fail_mode(influence_diagram, caplog):
    # Test is only reproducing result, not testing logic!
    with pytest.raises(Exception) as exc_info:
        InfluenceDiagramToDecisionTree().calculate_partial_order(
            influence_diagram, mode="junk"
        )
    assert [r.msg for r in caplog.records] == [
        "output mode should be [view|copy] and have been entered as junk"
    ]
    assert (
        str(exc_info.value)
        == "output mode should be [view|copy] and have been entered as junk"
    )


def test_calculate_partial_order_copy_mode(influence_diagram):
    # Test is only reproducing result, not testing logic!
    partial_order_0 = InfluenceDiagramToDecisionTree().calculate_partial_order(
        influence_diagram, mode="view"
    )
    partial_order = InfluenceDiagramToDecisionTree().calculate_partial_order(
        influence_diagram, mode="copy"
    )
    result = [n.shortname for n in partial_order]
    target = ["u1", "u2", "u3", "d1", "u4", "d2", "u5", "u6", "u7", "u8"]
    assert result == target
    assert partial_order_0 != partial_order


def test_output_branches_from_node_empty_lists(influence_diagram):
    uncertainty_node = influence_diagram.nodes[0]
    decision_node = influence_diagram.nodes[4]
    utility_node = influence_diagram.nodes[10]

    assert (
        len(
            list(
                zip(
                    *InfluenceDiagramToDecisionTree()._output_branches_from_node(
                        uncertainty_node, uncertainty_node
                    ),
                    strict=False,
                )
            )
        )
        == 0
    )
    assert (
        len(
            list(
                zip(
                    *InfluenceDiagramToDecisionTree()._output_branches_from_node(
                        decision_node, uncertainty_node
                    ),
                    strict=False,
                )
            )
        )
        == 0
    )
    assert (
        len(
            list(
                zip(
                    *InfluenceDiagramToDecisionTree()._output_branches_from_node(
                        utility_node, uncertainty_node
                    ),
                    strict=False,
                )
            )
        )
        == 0
    )


def test_output_branches_from_node(influence_diagram):
    uncertainty_node = influence_diagram.nodes[0]
    uncertainty_node._probability = DiscreteUnconditionalProbability(
        **{
            "probability_function": np.array([[0.7], [0.2], [0.1]]),
            "variables": {"States": ["pear", "lemon", "plum"]},
        }
    )
    decision_node = influence_diagram.nodes[4]
    decision_node._alternatives = ["wait", "pickup"]
    utility_node = influence_diagram.nodes[10]
    utility_node._utility = ["1000"]

    result = list(
        InfluenceDiagramToDecisionTree()._output_branches_from_node(
            uncertainty_node, uncertainty_node
        )
    )
    assert all(r[1] == uncertainty_node for r in result)
    assert [r[0].label for r in result] == ["plum", "lemon", "pear"]
    assert all(isinstance(r[0], Arc) for r in result)
    assert all(r[0].tail == uncertainty_node for r in result)
    assert all(r[0].head is None for r in result)

    result = list(
        InfluenceDiagramToDecisionTree()._output_branches_from_node(
            decision_node, uncertainty_node
        )
    )
    assert all(r[1] == uncertainty_node for r in result)
    assert [r[0].label for r in result] == ["pickup", "wait"]
    assert all(isinstance(r[0], Arc) for r in result)
    assert all(r[0].tail == decision_node for r in result)
    assert all(r[0].head is None for r in result)

    result = list(
        InfluenceDiagramToDecisionTree()._output_branches_from_node(
            utility_node, uncertainty_node
        )
    )
    assert all(r[1] == uncertainty_node for r in result)
    assert [r[0].label for r in result] == ["1000"]
    assert all(isinstance(r[0], Arc) for r in result)
    assert all(r[0].tail == utility_node for r in result)
    assert all(r[0].head is None for r in result)


def test_output_branches_from_node_reverse_mode(influence_diagram):
    uncertainty_node = influence_diagram.nodes[0]
    uncertainty_node._probability = DiscreteUnconditionalProbability(
        **{
            "probability_function": np.array([[0.7], [0.2], [0.1]]),
            "variables": {"States": ["pear", "lemon", "plum"]},
        }
    )

    result = list(
        InfluenceDiagramToDecisionTree()._output_branches_from_node(
            uncertainty_node, uncertainty_node, flip=False
        )
    )
    assert [r[0].label for r in result] == ["pear", "lemon", "plum"]


def test_convert_to_decision_tree_symmetry():
    # Medical Diagnosis Problem
    # Data taken from
    # DECISION TREES AND INFLUENCE DIAGRAMS
    # Prakash P. Shenoy
    # Encyclopedia of Life Support Systems, U Derigs (ed.),
    # Optimization and Operations Research, Vol. 4, pp. 280–298, 2009
    #
    #
    # Probabilities in the ID to be updated!!!
    #
    # The produced tree may be flipped horizontally compared to the expected one

    probability_S = DiscreteUnconditionalProbability(
        **{
            "probability_function": np.array([[0.7], [0.3]]),
            "variables": {"State": ["yes", "no"]},
        }
    )
    probability_P = DiscreteUnconditionalProbability(
        **{
            "probability_function": np.array([[0.2], [0.8]]),
            "variables": {"State": ["yes", "no"]},
        }
    )
    probability_D = DiscreteUnconditionalProbability(
        **{
            "probability_function": np.array([[0.1], [0.9]]),
            "variables": {"State": ["yes", "no"]},
        }
    )

    id_decision_T = DecisionNode(
        shortname="T", description="Treat for Disease", alternatives=["yes", "no"]
    )
    id_uncertainty_S = UncertaintyNode(
        shortname="S", description="Symptom", probability=probability_S
    )
    id_uncertainty_P = UncertaintyNode(
        shortname="P", description="Pathological state", probability=probability_P
    )
    id_uncertainty_D = UncertaintyNode(
        shortname="D", description="Disease", probability=probability_D
    )
    id_utility_0 = UtilityNode(shortname="v", description="Utility")

    id_e0 = Arc(tail=id_uncertainty_S, head=id_decision_T)
    id_e1 = Arc(tail=id_uncertainty_P, head=id_uncertainty_S)
    id_e2 = Arc(tail=id_uncertainty_D, head=id_uncertainty_P)
    id_e3 = Arc(tail=id_decision_T, head=id_utility_0)
    id_e4 = Arc(tail=id_uncertainty_P, head=id_utility_0)
    id_e5 = Arc(tail=id_uncertainty_D, head=id_utility_0)

    net = {
        "nodes": [
            id_decision_T,
            id_uncertainty_S,
            id_uncertainty_P,
            id_uncertainty_D,
            id_utility_0,
        ],
        "arcs": [id_e0, id_e1, id_e2, id_e3, id_e4, id_e5],
    }

    ID = InfluenceDiagram()
    ID.add_nodes(net["nodes"])
    ID.add_arcs(net["arcs"])

    dt_uncertainty_S = UncertaintyNode(
        shortname="S", description="Symptom", probability=probability_S
    )
    dt_decision_T_0 = DecisionNode(
        shortname="T", description="Treat for Disease", alternatives=["yes", "no"]
    )
    dt_e0 = Arc(tail=dt_uncertainty_S, head=dt_decision_T_0, label="yes")
    dt_uncertainty_P_0 = UncertaintyNode(
        shortname="P", description="Pathological state", probability=probability_P
    )
    dt_e1 = Arc(tail=dt_decision_T_0, head=dt_uncertainty_P_0, label="yes")
    dt_uncertainty_D_0 = UncertaintyNode(
        shortname="D", description="Disease", probability=probability_D
    )
    dt_e2 = Arc(tail=dt_uncertainty_P_0, head=dt_uncertainty_D_0, label="yes")
    dt_utility_0 = UtilityNode(shortname="v", description="Utility")
    dt_e3 = Arc(tail=dt_uncertainty_D_0, head=dt_utility_0, label="yes")
    dt_utility_1 = UtilityNode(shortname="v", description="Utility")
    dt_e4 = Arc(tail=dt_uncertainty_D_0, head=dt_utility_1, label="no")
    dt_uncertainty_D_1 = UncertaintyNode(
        shortname="D", description="Disease", probability=probability_D
    )
    dt_e5 = Arc(tail=dt_uncertainty_P_0, head=dt_uncertainty_D_1, label="no")
    dt_utility_2 = UtilityNode(shortname="v", description="Utility")
    dt_e6 = Arc(tail=dt_uncertainty_D_1, head=dt_utility_2, label="yes")
    dt_utility_3 = UtilityNode(shortname="v", description="Utility")
    dt_e7 = Arc(tail=dt_uncertainty_D_1, head=dt_utility_3, label="no")
    dt_uncertainty_P_1 = UncertaintyNode(
        shortname="P", description="Pathological state", probability=probability_P
    )
    dt_e8 = Arc(tail=dt_decision_T_0, head=dt_uncertainty_P_1, label="no")
    dt_uncertainty_D_2 = UncertaintyNode(
        shortname="D", description="Disease", probability=probability_D
    )
    dt_e9 = Arc(tail=dt_uncertainty_P_1, head=dt_uncertainty_D_2, label="yes")
    dt_utility_4 = UtilityNode(shortname="v", description="Utility")
    dt_e10 = Arc(tail=dt_uncertainty_D_2, head=dt_utility_4, label="yes")
    dt_utility_5 = UtilityNode(shortname="v", description="Utility")
    dt_e11 = Arc(tail=dt_uncertainty_D_2, head=dt_utility_5, label="no")
    dt_uncertainty_D_3 = UncertaintyNode(
        shortname="D", description="Disease", probability=probability_D
    )
    dt_e12 = Arc(tail=dt_uncertainty_P_1, head=dt_uncertainty_D_3, label="no")
    dt_utility_6 = UtilityNode(shortname="v", description="Utility")
    dt_e13 = Arc(tail=dt_uncertainty_D_3, head=dt_utility_6, label="yes")
    dt_utility_7 = UtilityNode(shortname="v", description="Utility")
    dt_e14 = Arc(tail=dt_uncertainty_D_3, head=dt_utility_7, label="no")
    dt_decision_T_1 = DecisionNode(
        shortname="T", description="Treat for Disease", alternatives=["yes", "no"]
    )
    dt_e15 = Arc(tail=dt_uncertainty_S, head=dt_decision_T_1, label="no")
    dt_uncertainty_P_2 = UncertaintyNode(
        shortname="P", description="Pathological state", probability=probability_P
    )
    dt_e16 = Arc(tail=dt_decision_T_1, head=dt_uncertainty_P_2, label="yes")
    dt_uncertainty_D_4 = UncertaintyNode(
        shortname="D", description="Disease", probability=probability_D
    )
    dt_e17 = Arc(tail=dt_uncertainty_P_2, head=dt_uncertainty_D_4, label="yes")
    dt_utility_8 = UtilityNode(shortname="v", description="Utility")
    dt_e18 = Arc(tail=dt_uncertainty_D_4, head=dt_utility_8, label="yes")
    dt_utility_9 = UtilityNode(shortname="v", description="Utility")
    dt_e19 = Arc(tail=dt_uncertainty_D_4, head=dt_utility_9, label="no")
    dt_uncertainty_D_5 = UncertaintyNode(
        shortname="D", description="Disease", probability=probability_D
    )
    dt_e20 = Arc(tail=dt_uncertainty_P_2, head=dt_uncertainty_D_5, label="no")
    dt_utility_10 = UtilityNode(shortname="v", description="Utility")
    dt_e21 = Arc(tail=dt_uncertainty_D_5, head=dt_utility_10, label="yes")
    dt_utility_11 = UtilityNode(shortname="v", description="Utility")
    dt_e22 = Arc(tail=dt_uncertainty_D_5, head=dt_utility_11, label="no")
    dt_uncertainty_P_3 = UncertaintyNode(
        shortname="P", description="Pathological state", probability=probability_P
    )
    dt_e23 = Arc(tail=dt_decision_T_1, head=dt_uncertainty_P_3, label="no")
    dt_uncertainty_D_6 = UncertaintyNode(
        shortname="D", description="Disease", probability=probability_D
    )
    dt_e24 = Arc(tail=dt_uncertainty_P_3, head=dt_uncertainty_D_6, label="yes")
    dt_utility_12 = UtilityNode(shortname="v", description="Utility")
    dt_e25 = Arc(tail=dt_uncertainty_D_6, head=dt_utility_12, label="yes")
    dt_utility_13 = UtilityNode(shortname="v", description="Utility")
    dt_e26 = Arc(tail=dt_uncertainty_D_6, head=dt_utility_13, label="no")
    dt_uncertainty_D_7 = UncertaintyNode(
        shortname="D", description="Disease", probability=probability_D
    )
    dt_e27 = Arc(tail=dt_uncertainty_P_3, head=dt_uncertainty_D_7, label="no")
    dt_utility_14 = UtilityNode(shortname="v", description="Utility")
    dt_e28 = Arc(tail=dt_uncertainty_D_7, head=dt_utility_14, label="yes")
    dt_utility_15 = UtilityNode(shortname="v", description="Utility")
    dt_e29 = Arc(tail=dt_uncertainty_D_7, head=dt_utility_15, label="no")

    nodes = [
        dt_uncertainty_S,
        dt_decision_T_0,
        dt_uncertainty_P_0,
        dt_uncertainty_D_0,
        dt_utility_0,
        dt_utility_1,
        dt_uncertainty_D_1,
        dt_utility_2,
        dt_utility_3,
        dt_uncertainty_P_1,
        dt_uncertainty_D_2,
        dt_utility_4,
        dt_utility_5,
        dt_uncertainty_D_3,
        dt_utility_6,
        dt_utility_7,
        dt_decision_T_1,
        dt_uncertainty_P_2,
        dt_uncertainty_D_4,
        dt_utility_8,
        dt_utility_9,
        dt_uncertainty_D_5,
        dt_utility_10,
        dt_utility_11,
        dt_uncertainty_P_3,
        dt_uncertainty_D_6,
        dt_utility_12,
        dt_utility_13,
        dt_uncertainty_D_7,
        dt_utility_14,
        dt_utility_15,
    ]
    net = {
        "nodes": nodes,
        "arcs": [
            dt_e0,
            dt_e1,
            dt_e2,
            dt_e3,
            dt_e4,
            dt_e5,
            dt_e6,
            dt_e7,
            dt_e8,
            dt_e9,
            dt_e10,
            dt_e11,
            dt_e12,
            dt_e13,
            dt_e14,
            dt_e15,
            dt_e16,
            dt_e17,
            dt_e18,
            dt_e19,
            dt_e20,
            dt_e21,
            dt_e22,
            dt_e23,
            dt_e24,
            dt_e25,
            dt_e26,
            dt_e27,
            dt_e28,
            dt_e29,
        ],
    }

    DT = DecisionTree(root=dt_uncertainty_S)
    DT.add_nodes(net["nodes"])
    DT.add_arcs(net["arcs"])

    IDT = InfluenceDiagramToDecisionTree().conversion(ID)
    for id_node, dt_node in zip(IDT.graph.nodes, DT.graph.nodes, strict=False):
        assert type(id_node) is type(dt_node)
        assert id_node.description == dt_node.description
        if not isinstance(id_node, UtilityNode):
            assert id_node.shortname == dt_node.shortname

    for id_edge, dt_edge in zip(IDT.graph.edges, DT.graph.edges, strict=False):
        assert type(id_edge) is type(dt_edge)
        assert id_edge[0].description == dt_edge[0].description
        assert id_edge[1].description == dt_edge[1].description
        assert (
            IDT.graph.edges[id_edge[0], id_edge[1]]["label"]
            == DT.graph.edges[dt_edge[0], dt_edge[1]]["label"]
        )
        assert (
            IDT.graph.edges[id_edge[0], id_edge[1]]["dtype"]
            == DT.graph.edges[dt_edge[0], dt_edge[1]]["dtype"]
        )


def test_convert_to_decision_tree_simple_order_asymmetry():
    probability_U1 = DiscreteUnconditionalProbability(
        **{
            "probability_function": np.array([[0.7], [0.3]]),
            "variables": {"State": ["high", "low"]},
        }
    )
    probability_U2 = DiscreteUnconditionalProbability(
        **{
            "probability_function": np.array([[0.2], [0.8]]),
            "variables": {"State": ["yes", "no"]},
        }
    )

    id_uncertainty_u1 = UncertaintyNode(
        shortname="u1", description="U1", probability=probability_U1
    )
    id_uncertainty_u2 = UncertaintyNode(
        shortname="u2", description="U2", probability=probability_U2
    )
    id_decision = DecisionNode(
        shortname="D", description="D", alternatives=["green", "red"]
    )

    id_e0 = Arc(tail=id_uncertainty_u1, head=id_decision)
    id_e1 = Arc(tail=id_uncertainty_u2, head=id_decision)

    net = {
        "nodes": [id_uncertainty_u1, id_uncertainty_u2, id_decision],
        "arcs": [id_e0, id_e1],
    }

    ID = InfluenceDiagram()
    ID.add_nodes(net["nodes"])
    ID.add_arcs(net["arcs"])

    dt_uncertainty_u1 = UncertaintyNode(
        shortname="u1", description="U1", probability=probability_U1
    )

    dt_uncertainty_u2_1 = UncertaintyNode(
        shortname="u2", description="U2", probability=probability_U2
    )
    dt_e0 = Arc(tail=dt_uncertainty_u1, head=dt_uncertainty_u2_1, label="high")
    dt_decision_1 = DecisionNode(
        shortname="D", description="D", alternatives=["green", "red"]
    )
    dt_e1 = Arc(tail=dt_uncertainty_u2_1, head=dt_decision_1, label="yes")
    dt_utility_0 = UtilityNode(shortname="v", description="Utility")
    dt_e2 = Arc(tail=dt_decision_1, head=dt_utility_0, label="green")
    dt_utility_1 = UtilityNode(shortname="v", description="Utility")
    dt_e3 = Arc(tail=dt_decision_1, head=dt_utility_1, label="red")

    dt_decision_2 = DecisionNode(
        shortname="D", description="D", alternatives=["green", "red"]
    )
    dt_e4 = Arc(tail=dt_uncertainty_u2_1, head=dt_decision_2, label="no")
    dt_utility_2 = UtilityNode(shortname="v", description="Utility")
    dt_e5 = Arc(tail=dt_decision_2, head=dt_utility_2, label="green")
    dt_utility_3 = UtilityNode(shortname="v", description="Utility")
    dt_e6 = Arc(tail=dt_decision_2, head=dt_utility_3, label="red")

    dt_uncertainty_u2_2 = UncertaintyNode(
        shortname="u2", description="U2", probability=probability_U2
    )
    dt_e7 = Arc(tail=dt_uncertainty_u1, head=dt_uncertainty_u2_2, label="low")
    dt_decision_3 = DecisionNode(
        shortname="D", description="D", alternatives=["green", "red"]
    )
    dt_e8 = Arc(tail=dt_uncertainty_u2_2, head=dt_decision_3, label="yes")
    dt_utility_4 = UtilityNode(shortname="v", description="Utility")
    dt_e9 = Arc(tail=dt_decision_3, head=dt_utility_4, label="green")
    dt_utility_5 = UtilityNode(shortname="v", description="Utility")
    dt_e10 = Arc(tail=dt_decision_3, head=dt_utility_5, label="red")

    dt_decision_4 = DecisionNode(
        shortname="D", description="D", alternatives=["green", "red"]
    )
    dt_e11 = Arc(tail=dt_uncertainty_u2_2, head=dt_decision_4, label="no")
    dt_utility_6 = UtilityNode(shortname="v", description="Utility")
    dt_e12 = Arc(tail=dt_decision_4, head=dt_utility_6, label="green")
    dt_utility_7 = UtilityNode(shortname="v", description="Utility")
    dt_e13 = Arc(tail=dt_decision_4, head=dt_utility_7, label="red")

    nodes = [
        dt_uncertainty_u1,
        dt_uncertainty_u2_1,
        dt_decision_1,
        dt_utility_0,
        dt_utility_1,
        dt_decision_2,
        dt_utility_2,
        dt_utility_3,
        dt_uncertainty_u2_2,
        dt_decision_3,
        dt_utility_4,
        dt_utility_5,
        dt_decision_4,
        dt_utility_6,
        dt_utility_7,
    ]
    net = {
        "nodes": nodes,
        "arcs": [
            dt_e0,
            dt_e1,
            dt_e2,
            dt_e3,
            dt_e4,
            dt_e5,
            dt_e6,
            dt_e7,
            dt_e8,
            dt_e9,
            dt_e10,
            dt_e11,
            dt_e12,
            dt_e13,
        ],
    }

    DT = DecisionTree(root=dt_uncertainty_u1)
    DT.add_nodes(net["nodes"])
    DT.add_arcs(net["arcs"])

    IDT = InfluenceDiagramToDecisionTree().conversion(ID)
    for id_node, dt_node in zip(IDT.graph.nodes, DT.graph.nodes, strict=False):
        assert type(id_node) is type(dt_node)
        assert id_node.description == dt_node.description
        if not isinstance(id_node, UtilityNode):
            assert id_node.shortname == dt_node.shortname

    for id_edge, dt_edge in zip(IDT.graph.edges, DT.graph.edges, strict=False):
        assert type(id_edge) is type(dt_edge)
        assert id_edge[0].description == dt_edge[0].description
        assert id_edge[1].description == dt_edge[1].description
        assert (
            IDT.graph.edges[id_edge[0], id_edge[1]]["label"]
            == DT.graph.edges[dt_edge[0], dt_edge[1]]["label"]
        )
        assert (
            IDT.graph.edges[id_edge[0], id_edge[1]]["dtype"]
            == DT.graph.edges[dt_edge[0], dt_edge[1]]["dtype"]
        )


# def test_convert_to_decision_tree_asymemetry():
#  TEST NEEDS TO BE UPDATED !!!

#   # Wildcatter example
#   # Data taken from
#   # An improved method for solving Hybrid Influence Diagrams
#   # Barbaros Yet, Martin Neil, Norman Fenton, Anthony Constantinou,
#   # Eugene Dementiev
#   # International Journal of Approximate Reasoning, Volume 95, April 2018,
#   # Pages 93-112
#   # https://doi.org/10.1016/j.ijar.2018.01.006
#   #
#   #
#   # Probabilities in the ID to be updated!!!
#   #
#   # The produced tree may be flipped horizontally compared to the expected one
#   id_decision_T = DecisionNode("Seismic Test", "T", alternatives=["yes", "No"])
#   id_decision_D = DecisionNode("Drill", "D", alternatives=["yes", "No"])
#   id_uncertainty_R = UncertaintyNode("Test Result", "R", \
#                  probabilities={'No': 0.410, 'Open': 0.350, 'Closed': 0.240})
#   id_uncertainty_O = UncertaintyNode("Oil", "O", \
#                  probabilities={'Dry': 0.7, 'Wet': 0.2, 'Soaking': 0.1})
#   id_value_S = UtilityNode("Seismic Cost", "U1", utility=0)
#   id_value_D = UtilityNode("Drilling Gain", "U2", utility=0)
#   id_value_T = UtilityNode("Total", "U3", utility=0)

#   id_edge_0 = Edge(id_decision_T, id_value_S)
#   id_edge_1 = Edge(id_decision_T, id_uncertainty_R)
#   id_edge_2 = Edge(id_decision_T, id_decision_D)
#   id_edge_3 = Edge(id_uncertainty_R, id_decision_D)
#   id_edge_4 = Edge(id_uncertainty_O, id_uncertainty_R)
#   id_edge_5 = Edge(id_uncertainty_O, id_value_D)
#   id_edge_6 = Edge(id_decision_D, id_value_D)
#   id_edge_7 = Edge(id_value_S, id_value_T)
#   id_edge_8 = Edge(id_value_D, id_value_T)

#   net = {'nodes': [id_decision_T, id_decision_D, id_uncertainty_R, \
#                        id_uncertainty_O, id_value_S, id_value_D, id_value_T],
#          'edges': [id_edge_0, id_edge_1, id_edge_2, id_edge_3, id_edge_4, \
#                        id_edge_5, id_edge_6, id_edge_7, id_edge_8]}

#   ID = InfluenceDiagram()
#   for node in net['nodes']:
#       ID.add_node(node)
#   for edge in net['edges']:
#       ID.add_edge(edge)


#   dt_decision_T_0 = DecisionNode("Seismic Test", "T", alternatives=["yes", "No"])
#   dt_decision_R_0 = UncertaintyNode("Test Result", "R", \
#                     probabilities={'No': 0.410, 'Open': 0.350, 'Closed': 0.240})
#   dt_edge_0 = Edge(dt_decision_T_0, dt_decision_R_0, name="Yes")
#   dt_decision_D_0 = DecisionNode("Drill", "D", alternatives=["yes", "No"])
#   dt_edge_1 = Edge(dt_decision_R_0, dt_decision_D_0, name="No")
#   dt_uncertainty_O_0 = UncertaintyNode("Oil", "O", \
#                     probabilities={'Dry': 0.7, 'Wet': 0.2, 'Soaking': 0.1})
#   dt_edge_2 = Edge(dt_decision_D_0, dt_uncertainty_O_0, name="Yes")
#   dt_value_T_0 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_3 = Edge(dt_uncertainty_O_0, dt_value_T_0, name="Dry")
#   dt_value_T_1 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_4 = Edge(dt_uncertainty_O_0, dt_value_T_1, name="Wet")
#   dt_value_T_2 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_5 = Edge(dt_uncertainty_O_0, dt_value_T_2, name="Soaking")
#   dt_value_T_3 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_6 = Edge(dt_decision_D_0, dt_value_T_3, name="No")
#   dt_decision_D_1 = DecisionNode("Drill", "D", alternatives=["yes", "No"])
#   dt_edge_7 = Edge(dt_decision_R_0, dt_decision_D_1, name="Open")
#   dt_uncertainty_O_1 = UncertaintyNode("Oil", "O", \
#                     probabilities={'Dry': 0.7, 'Wet': 0.2, 'Soaking': 0.1})
#   dt_edge_8 = Edge(dt_decision_D_1, dt_uncertainty_O_1, name="Yes")
#   dt_value_T_4 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_9 = Edge(dt_uncertainty_O_1, dt_value_T_4, name="Dry")
#   dt_value_T_5 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_10 = Edge(dt_uncertainty_O_1, dt_value_T_5, name="Wet")
#   dt_value_T_6 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_11 = Edge(dt_uncertainty_O_1, dt_value_T_6, name="Soaking")
#   dt_value_T_7 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_12 = Edge(dt_decision_D_1, dt_value_T_7, name="No")
#   dt_decision_D_2 = DecisionNode("Drill", "D", alternatives=["yes", "No"])
#   dt_edge_13 = Edge(dt_decision_R_0, dt_decision_D_2, name="Closed")
#   dt_uncertainty_O_2 = UncertaintyNode("Oil", "O", \
#                     probabilities={'Dry': 0.7, 'Wet': 0.2, 'Soaking': 0.1})
#   dt_edge_14 = Edge(dt_decision_D_2, dt_uncertainty_O_2, name="Yes")
#   dt_value_T_8 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_15 = Edge(dt_uncertainty_O_2, dt_value_T_8, name="Dry")
#   dt_value_T_9 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_16 = Edge(dt_uncertainty_O_2, dt_value_T_9, name="Wet")
#   dt_value_T_10 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_17 = Edge(dt_uncertainty_O_2, dt_value_T_10, name="Soaking")
#   dt_value_T_11 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_18 = Edge(dt_decision_D_2, dt_value_T_11, name="No")
#   dt_decision_D_3 = DecisionNode("Drill", "D", alternatives=["yes", "No"])
#   dt_edge_19 = Edge(dt_decision_T_0, dt_decision_D_3, name="No")
#   dt_uncertainty_O_3 = UncertaintyNode("Oil", "O", \
#                     probabilities={'Dry': 0.7, 'Wet': 0.2, 'Soaking': 0.1})
#   dt_edge_20 = Edge(dt_decision_D_2, dt_uncertainty_O_3, name="Yes")
#   dt_value_T_12 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_21 = Edge(dt_uncertainty_O_3, dt_value_T_12, name="Dry")
#   dt_value_T_13 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_22 = Edge(dt_uncertainty_O_3, dt_value_T_13, name="Wet")
#   dt_value_T_14 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_23 = Edge(dt_uncertainty_O_3, dt_value_T_14, name="Soaking")
#   dt_value_T_15 = UtilityNode("Total", "U3", utility=0)
#   dt_edge_24 = Edge(dt_decision_D_3, dt_value_T_15, name="No")


#   net = {'nodes': [dt_decision_T_0,
#                    dt_decision_R_0,
#                    dt_decision_D_0,
#                    dt_uncertainty_O_0,
#                    dt_value_T_0,
#                    dt_value_T_1,
#                    dt_value_T_2,
#                    dt_value_T_3,
#                    dt_decision_D_1,
#                    dt_uncertainty_O_1,
#                    dt_value_T_4,
#                    dt_value_T_5,
#                    dt_value_T_6,
#                    dt_value_T_7,
#                    dt_decision_D_2,
#                    dt_uncertainty_O_2,
#                    dt_value_T_8,
#                    dt_value_T_9,
#                    dt_value_T_10,
#                    dt_value_T_11,
#                    dt_decision_D_3,
#                    dt_uncertainty_O_3,
#                    dt_value_T_12,
#                    dt_value_T_13,
#                    dt_value_T_14,
#                    dt_value_T_15],
#          'edges': [dt_edge_0,
#                    dt_edge_1,
#                    dt_edge_2,
#                    dt_edge_3,
#                    dt_edge_4,
#                    dt_edge_5,
#                    dt_edge_6,
#                    dt_edge_7,
#                    dt_edge_8,
#                    dt_edge_8,
#                    dt_edge_9,
#                    dt_edge_10,
#                    dt_edge_11,
#                    dt_edge_12,
#                    dt_edge_13,
#                    dt_edge_14,
#                    dt_edge_15,
#                    dt_edge_16,
#                    dt_edge_17,
#                    dt_edge_18,
#                    dt_edge_19,
#                    dt_edge_20,
#                    dt_edge_21,
#                    dt_edge_22,
#                    dt_edge_23,
#                    dt_edge_24]}

#   DT = DecisionTree()
#   for node in net['nodes']:
#       DT.add_node(node)
#   for edge in net['edges']:
#       DT.add_edge(edge)

#   assert ID.convert_to_decision_tree() == DT
