import json

import networkx as nx
import pyAgrum as gum
import pytest

from src.v0.models.issue import ProbabilityData
from src.v0.models.structure import InfluenceDiagramResponse
from src.v0.services.structure_utils.decision_diagrams.decision_tree import DecisionTree
from src.v0.services.structure_utils.decision_diagrams.edge import Edge
from src.v0.services.structure_utils.decision_diagrams.influence_diagram import (
    InfluenceDiagram,
)
from src.v0.services.structure_utils.decision_diagrams.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
)
from src.v0.services.structure_utils.probability.discrete_unconditional_probability import (  # noqa: E501
    DiscreteUnconditionalProbability,
)

TESTDATA = "v0/services/testdata"


@pytest.fixture
def graph_as_dict():
    n0 = UncertaintyNode("u1", "Uncertainty node 1")
    n1 = UncertaintyNode("u2", "Uncertainty node 2")
    n2 = UncertaintyNode("u3", "Uncertainty node 3")
    n3 = UncertaintyNode("u4", "Uncertainty node 4")
    n4 = DecisionNode("d1", "Decision node 1")
    n5 = UncertaintyNode("u5", "Uncertainty node 5")
    n6 = DecisionNode("d2", "Decision node 2")
    n7 = UncertaintyNode("u6", "Uncertainty node 6")
    n8 = UncertaintyNode("u7", "Uncertainty node 7")
    n9 = UncertaintyNode("u8", "Uncertainty node 8")
    n10 = UtilityNode("v1", "Utility node 1")

    e0 = Edge(n0, n4, name="e0")
    e1 = Edge(n1, n4, name="e1")
    e2 = Edge(n2, n4, name="e2")
    e3 = Edge(n3, n6, name="e3")
    e4 = Edge(n4, n6, name="e4")
    e5 = Edge(n4, n5, name="e5")
    e6 = Edge(n6, n7, name="e6")
    e7 = Edge(n6, n8, name="e7")
    e8 = Edge(n6, n9, name="e8")
    e9 = Edge(n5, n10, name="e9")

    return {
        "nodes": [n0, n1, n2, n3, n4, n5, n6, n7, n8, n9, n10],
        "edges": [e0, e1, e2, e3, e4, e5, e6, e7, e8, e9],
    }


def test_from_dict(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    assert isinstance(ID.nx, nx.DiGraph)
    assert ID.decision_count == 2
    assert ID.uncertainty_count == 8
    assert ID.utility_count == 1


def test_from_db(copy_testdata_tmpdir, tmp_path):
    copy_testdata_tmpdir(TESTDATA)
    with open(tmp_path / "used_car_buyer_model_response.json") as f:
        json_stream = json.load(f)
    influence_diagram_response = InfluenceDiagramResponse(
        vertices=json_stream["vertices"], edges=json_stream["edges"]
    )
    InfluenceDiagram.from_db(influence_diagram_response)

    n0 = UncertaintyNode("State", "Joe does not know the state of the car")
    n1 = UncertaintyNode("Test Result", "The result of the test is currently unknown")
    n2 = DecisionNode("Buy", "We can buy the car")
    n3 = DecisionNode("Test", "Joe can test the car")
    n4 = UtilityNode("Value", "Value")

    e0 = Edge(n2, n4, name="e0")
    e1 = Edge(n0, n1, name="e1")
    e2 = Edge(n0, n4, name="e2")
    e3 = Edge(n1, n2, name="e3")
    e4 = Edge(n3, n1, name="e4")

    target = InfluenceDiagram.from_dict(
        {"nodes": [n0, n1, n2, n3, n4], "edges": [e0, e1, e2, e3, e4]}
    )
    result = InfluenceDiagram.from_db(influence_diagram_response)

    for result_node, target_node in zip(result.nx.nodes, target.nx.nodes, strict=False):
        assert type(result_node) is type(target_node)
        assert result_node.description == target_node.description
        if not isinstance(result_node, UtilityNode):
            assert result_node.shortname == target_node.shortname

    for result_arc, target_arc in zip(result.nx.edges, target.nx.edges, strict=False):
        assert type(result_arc) is type(target_arc)
        assert result_arc[0].description == target_arc[0].description
        assert result_arc[1].description == target_arc[1].description
        assert (
            result.nx.edges[result_arc[0], result_arc[1]]["arc_type"]
            == target.nx.edges[target_arc[0], target_arc[1]]["arc_type"]
        )


def test_to_json(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    result = ID.to_json()
    json_result = json.loads(result)
    assert json_result["directed"]
    assert not json_result["multigraph"]
    assert len(json_result["nodes"]) == 11
    assert len(json_result["edges"]) == 10
    assert result.count("description") == 11
    assert result.count("shortname") == 11
    assert result.count("from") == 10
    assert result.count("to") == 10


def test_class_InfluenceDiagram():
    ID = InfluenceDiagram()
    assert isinstance(ID.nx, nx.DiGraph)


def test_copy():
    ID = InfluenceDiagram()
    assert nx.utils.graphs_equal(ID.nx, ID.copy().nx)


def test_get_parents(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    n4 = graph_as_dict["nodes"][4]
    result = ID.get_parents(n4)
    target = graph_as_dict["nodes"][0:3]
    assert result == target


def test_get_children(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    n6 = graph_as_dict["nodes"][6]
    result = ID.get_children(n6)
    target = graph_as_dict["nodes"][7:10]
    assert result == target

    n4 = graph_as_dict["nodes"][4]
    result = ID.get_children(n4)
    target = [graph_as_dict["nodes"][5], graph_as_dict["nodes"][6]]
    assert all(item in target for item in result)
    assert all(item in result for item in target)


def test_get_node_type(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    n6 = graph_as_dict["nodes"][6]
    assert ID.get_node_type(n6) == "decision"


def test_get_nodes_from_type(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    assert ID._get_nodes_from_type("DecisionNode") == [
        graph_as_dict["nodes"][4],
        graph_as_dict["nodes"][6],
    ]
    assert ID._get_nodes_from_type("UtilityNode") == [graph_as_dict["nodes"][10]]
    assert ID._get_nodes_from_type("UncertaintyNode") == [
        graph_as_dict["nodes"][0],
        graph_as_dict["nodes"][1],
        graph_as_dict["nodes"][2],
        graph_as_dict["nodes"][3],
        graph_as_dict["nodes"][5],
        graph_as_dict["nodes"][7],
        graph_as_dict["nodes"][8],
        graph_as_dict["nodes"][9],
    ]


def test_get_decision_nodes(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    assert ID.get_decision_nodes() == [
        graph_as_dict["nodes"][4],
        graph_as_dict["nodes"][6],
    ]


def test_get_utility_nodes(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    assert ID.get_utility_nodes() == [graph_as_dict["nodes"][10]]


def test_get_uncertainty_nodes(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    assert ID.get_uncertainty_nodes() == [
        graph_as_dict["nodes"][0],
        graph_as_dict["nodes"][1],
        graph_as_dict["nodes"][2],
        graph_as_dict["nodes"][3],
        graph_as_dict["nodes"][5],
        graph_as_dict["nodes"][7],
        graph_as_dict["nodes"][8],
        graph_as_dict["nodes"][9],
    ]


def test_nodes_count(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    assert ID.decision_count == 2
    assert ID.utility_count == 1
    assert ID.uncertainty_count == 8


def test_has_children(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    n4 = graph_as_dict["nodes"][4]
    n8 = graph_as_dict["nodes"][8]
    assert ID.has_children(n4)
    assert not ID.has_children(n8)


def test_get_node_from_uuid(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    n4 = graph_as_dict["nodes"][4]
    uuid = n4.uuid
    node = ID.get_node_from_uuid(uuid)
    assert isinstance(node, DecisionNode)
    assert node.description == "Decision node 1"
    assert node.shortname == "d1"


def test_decision_elimination_order(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    result = ID.decision_elimination_order()
    target = [graph_as_dict["nodes"][4], graph_as_dict["nodes"][6]]
    assert all(item in target for item in result)
    assert all(item in result for item in target)


def test_calculate_partial_order(graph_as_dict):
    # Test is only reproducing result, not testing logic!
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    partial_order = ID.calculate_partial_order()
    result = [n.shortname for n in partial_order]
    target = ["u1", "u2", "u3", "d1", "u4", "d2", "u5", "u6", "u7", "u8"]
    assert result == target


def test_calculate_partial_order_fail_mode(graph_as_dict, caplog):
    # Test is only reproducing result, not testing logic!
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    with pytest.raises(Exception) as exc_info:
        ID.calculate_partial_order(mode="junk")
    assert [r.msg for r in caplog.records] == [
        "output mode should be [view|copy] and have been entered as junk"
    ]
    assert (
        str(exc_info.value)
        == "output mode should be [view|copy] and have been entered as junk"
    )


def test_calculate_partial_order_copy_mode(graph_as_dict):
    # Test is only reproducing result, not testing logic!
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    partial_order_0 = ID.calculate_partial_order(mode="view")
    partial_order = ID.calculate_partial_order(mode="copy")
    result = [n.shortname for n in partial_order]
    target = ["u1", "u2", "u3", "d1", "u4", "d2", "u5", "u6", "u7", "u8"]
    assert result == target
    assert partial_order_0 != partial_order


def test_output_branches_from_node_empty_lists(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    uncertainty_node = graph_as_dict["nodes"][0]
    decision_node = graph_as_dict["nodes"][4]
    utility_node = graph_as_dict["nodes"][10]

    assert (
        len(
            list(
                zip(
                    *ID._output_branches_from_node(uncertainty_node, uncertainty_node),
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
                    *ID._output_branches_from_node(decision_node, uncertainty_node),
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
                    *ID._output_branches_from_node(utility_node, uncertainty_node),
                    strict=False,
                )
            )
        )
        == 0
    )


def test_output_branches_from_node(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    probability = ProbabilityData(
        **{
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.7, 0.2, 0.1]],
            "variables": {"State": ["pear", "lemon", "plum"]},
        }
    )
    uncertainty_node = graph_as_dict["nodes"][0]
    uncertainty_node._probabilities = DiscreteUnconditionalProbability.from_db_model(
        probability
    )
    decision_node = graph_as_dict["nodes"][4]
    decision_node._alternatives = ["wait", "pickup"]
    utility_node = graph_as_dict["nodes"][10]
    utility_node._utility = ["1000"]

    result = list(ID._output_branches_from_node(uncertainty_node, uncertainty_node))
    assert all(r[1] == uncertainty_node for r in result)
    assert [r[0].name for r in result] == ["plum", "lemon", "pear"]
    assert all(isinstance(r[0], Edge) for r in result)
    assert all(r[0].endpoint_start == uncertainty_node for r in result)
    assert all(r[0].endpoint_end is None for r in result)

    result = list(ID._output_branches_from_node(decision_node, uncertainty_node))
    assert all(r[1] == uncertainty_node for r in result)
    assert [r[0].name for r in result] == ["pickup", "wait"]
    assert all(isinstance(r[0], Edge) for r in result)
    assert all(r[0].endpoint_start == decision_node for r in result)
    assert all(r[0].endpoint_end is None for r in result)

    result = list(ID._output_branches_from_node(utility_node, uncertainty_node))
    assert all(r[1] == uncertainty_node for r in result)
    assert [r[0].name for r in result] == ["1000"]
    assert all(isinstance(r[0], Edge) for r in result)
    assert all(r[0].endpoint_start == utility_node for r in result)
    assert all(r[0].endpoint_end is None for r in result)


def test_output_branches_from_node_reverse_mode(graph_as_dict):
    ID = InfluenceDiagram.from_dict(graph_as_dict)
    probability = ProbabilityData(
        **{
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.7, 0.2, 0.1]],
            "variables": {"State": ["pear", "lemon", "plum"]},
        }
    )
    uncertainty_node = graph_as_dict["nodes"][0]
    uncertainty_node._probabilities = DiscreteUnconditionalProbability.from_db_model(
        probability
    )

    result = list(
        ID._output_branches_from_node(uncertainty_node, uncertainty_node, flip=False)
    )
    assert [r[0].name for r in result] == ["pear", "lemon", "plum"]


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

    probability_S = ProbabilityData(
        **{
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [
                [
                    0.7,
                    0.3,
                ]
            ],
            "variables": {
                "State": [
                    "yes",
                    "no",
                ]
            },
        }
    )
    probability_S = DiscreteUnconditionalProbability.from_db_model(probability_S)
    probability_P = ProbabilityData(
        **{
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [
                [
                    0.2,
                    0.8,
                ]
            ],
            "variables": {
                "State": [
                    "yes",
                    "no",
                ]
            },
        }
    )
    probability_P = DiscreteUnconditionalProbability.from_db_model(probability_P)
    probability_D = ProbabilityData(
        **{
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [
                [
                    0.1,
                    0.9,
                ]
            ],
            "variables": {
                "State": [
                    "yes",
                    "no",
                ]
            },
        }
    )
    probability_D = DiscreteUnconditionalProbability.from_db_model(probability_D)

    id_decision_T = DecisionNode("T", "Treat for Disease", alternatives=["yes", "no"])
    id_uncertainty_S = UncertaintyNode("S", "Symptom", probabilities=probability_S)
    id_uncertainty_P = UncertaintyNode(
        "P", "Pathological state", probabilities=probability_P
    )
    id_uncertainty_D = UncertaintyNode("D", "Disease", probabilities=probability_D)
    id_utility_0 = UtilityNode("v", "Utility", utility=None)

    id_e0 = Edge(id_uncertainty_S, id_decision_T)
    id_e1 = Edge(id_uncertainty_P, id_uncertainty_S)
    id_e2 = Edge(id_uncertainty_D, id_uncertainty_P)
    id_e3 = Edge(id_decision_T, id_utility_0)
    id_e4 = Edge(id_uncertainty_P, id_utility_0)
    id_e5 = Edge(id_uncertainty_D, id_utility_0)

    net = {
        "nodes": [
            id_decision_T,
            id_uncertainty_S,
            id_uncertainty_P,
            id_uncertainty_D,
            id_utility_0,
        ],
        "edges": [id_e0, id_e1, id_e2, id_e3, id_e4, id_e5],
    }

    ID = InfluenceDiagram()
    for node in net["nodes"]:
        ID.add_node(node)
    for edge in net["edges"]:
        ID.add_edge(edge)

    dt_uncertainty_S = UncertaintyNode("S", "Symptom", probabilities=probability_S)
    dt_decision_T_0 = DecisionNode("T", "Treat for Disease", alternatives=["yes", "no"])
    dt_e0 = Edge(dt_uncertainty_S, dt_decision_T_0, name="yes")
    dt_uncertainty_P_0 = UncertaintyNode(
        "P", "Pathological state", probabilities=probability_P
    )
    dt_e1 = Edge(dt_decision_T_0, dt_uncertainty_P_0, name="yes")
    dt_uncertainty_D_0 = UncertaintyNode("D", "Disease", probabilities=probability_D)
    dt_e2 = Edge(dt_uncertainty_P_0, dt_uncertainty_D_0, name="yes")
    dt_utility_0 = UtilityNode("v", "Utility", utility=None)
    dt_e3 = Edge(dt_uncertainty_D_0, dt_utility_0, name="yes")
    dt_utility_1 = UtilityNode("v", "Utility", utility=None)
    dt_e4 = Edge(dt_uncertainty_D_0, dt_utility_1, name="no")
    dt_uncertainty_D_1 = UncertaintyNode("D", "Disease", probabilities=probability_D)
    dt_e5 = Edge(dt_uncertainty_P_0, dt_uncertainty_D_1, name="no")
    dt_utility_2 = UtilityNode("v", "Utility", utility=None)
    dt_e6 = Edge(dt_uncertainty_D_1, dt_utility_2, name="yes")
    dt_utility_3 = UtilityNode("v", "Utility", utility=None)
    dt_e7 = Edge(dt_uncertainty_D_1, dt_utility_3, name="no")
    dt_uncertainty_P_1 = UncertaintyNode(
        "P", "Pathological state", probabilities=probability_P
    )
    dt_e8 = Edge(dt_decision_T_0, dt_uncertainty_P_1, name="no")
    dt_uncertainty_D_2 = UncertaintyNode("D", "Disease", probabilities=probability_D)
    dt_e9 = Edge(dt_uncertainty_P_1, dt_uncertainty_D_2, name="yes")
    dt_utility_4 = UtilityNode("v", "Utility", utility=None)
    dt_e10 = Edge(dt_uncertainty_D_2, dt_utility_4, name="yes")
    dt_utility_5 = UtilityNode("v", "Utility", utility=None)
    dt_e11 = Edge(dt_uncertainty_D_2, dt_utility_5, name="no")
    dt_uncertainty_D_3 = UncertaintyNode("D", "Disease", probabilities=probability_D)
    dt_e12 = Edge(dt_uncertainty_P_1, dt_uncertainty_D_3, name="no")
    dt_utility_6 = UtilityNode("v", "Utility", utility=None)
    dt_e13 = Edge(dt_uncertainty_D_3, dt_utility_6, name="yes")
    dt_utility_7 = UtilityNode("v", "Utility", utility=None)
    dt_e14 = Edge(dt_uncertainty_D_3, dt_utility_7, name="no")
    dt_decision_T_1 = DecisionNode("T", "Treat for Disease", alternatives=["yes", "no"])
    dt_e15 = Edge(dt_uncertainty_S, dt_decision_T_1, name="no")
    dt_uncertainty_P_2 = UncertaintyNode(
        "P", "Pathological state", probabilities=probability_P
    )
    dt_e16 = Edge(dt_decision_T_1, dt_uncertainty_P_2, name="yes")
    dt_uncertainty_D_4 = UncertaintyNode("D", "Disease", probabilities=probability_D)
    dt_e17 = Edge(dt_uncertainty_P_2, dt_uncertainty_D_4, name="yes")
    dt_utility_8 = UtilityNode("v", "Utility", utility=None)
    dt_e18 = Edge(dt_uncertainty_D_4, dt_utility_8, name="yes")
    dt_utility_9 = UtilityNode("v", "Utility", utility=None)
    dt_e19 = Edge(dt_uncertainty_D_4, dt_utility_9, name="no")
    dt_uncertainty_D_5 = UncertaintyNode("D", "Disease", probabilities=probability_D)
    dt_e20 = Edge(dt_uncertainty_P_2, dt_uncertainty_D_5, name="no")
    dt_utility_10 = UtilityNode("v", "Utility", utility=None)
    dt_e21 = Edge(dt_uncertainty_D_5, dt_utility_10, name="yes")
    dt_utility_11 = UtilityNode("v", "Utility", utility=None)
    dt_e22 = Edge(dt_uncertainty_D_5, dt_utility_11, name="no")
    dt_uncertainty_P_3 = UncertaintyNode(
        "P", "Pathological state", probabilities=probability_P
    )
    dt_e23 = Edge(dt_decision_T_1, dt_uncertainty_P_3, name="no")
    dt_uncertainty_D_6 = UncertaintyNode("D", "Disease", probabilities=probability_D)
    dt_e24 = Edge(dt_uncertainty_P_3, dt_uncertainty_D_6, name="yes")
    dt_utility_12 = UtilityNode("v", "Utility", utility=None)
    dt_e25 = Edge(dt_uncertainty_D_6, dt_utility_12, name="yes")
    dt_utility_13 = UtilityNode("v", "Utility", utility=None)
    dt_e26 = Edge(dt_uncertainty_D_6, dt_utility_13, name="no")
    dt_uncertainty_D_7 = UncertaintyNode("D", "Disease", probabilities=probability_D)
    dt_e27 = Edge(dt_uncertainty_P_3, dt_uncertainty_D_7, name="no")
    dt_utility_14 = UtilityNode("v", "Utility", utility=None)
    dt_e28 = Edge(dt_uncertainty_D_7, dt_utility_14, name="yes")
    dt_utility_15 = UtilityNode("v", "Utility", utility=None)
    dt_e29 = Edge(dt_uncertainty_D_7, dt_utility_15, name="no")

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
        "edges": [
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
    for node in net["nodes"]:
        DT.add_node(node)
    for edge in net["edges"]:
        DT.add_edge(edge)

    IDT = ID.convert_to_decision_tree()
    for id_node, dt_node in zip(IDT.nx.nodes, DT.nx.nodes, strict=False):
        assert type(id_node) is type(dt_node)
        assert id_node.description == dt_node.description
        if not isinstance(id_node, UtilityNode):
            assert id_node.shortname == dt_node.shortname

    for id_edge, dt_edge in zip(IDT.nx.edges, DT.nx.edges, strict=False):
        assert type(id_edge) is type(dt_edge)
        assert id_edge[0].description == dt_edge[0].description
        assert id_edge[1].description == dt_edge[1].description
        assert (
            IDT.nx.edges[id_edge[0], id_edge[1]]["name"]
            == DT.nx.edges[dt_edge[0], dt_edge[1]]["name"]
        )
        assert (
            IDT.nx.edges[id_edge[0], id_edge[1]]["arc_type"]
            == DT.nx.edges[dt_edge[0], dt_edge[1]]["arc_type"]
        )


def test_convert_to_decision_tree_simple_order_asymmetry():
    probability_U1 = ProbabilityData(
        **{
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [
                [
                    0.7,
                    0.3,
                ]
            ],
            "variables": {
                "State": [
                    "high",
                    "low",
                ]
            },
        }
    )
    probability_U1 = DiscreteUnconditionalProbability.from_db_model(probability_U1)
    probability_U2 = ProbabilityData(
        **{
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [
                [
                    0.2,
                    0.8,
                ]
            ],
            "variables": {
                "State": [
                    "yes",
                    "no",
                ]
            },
        }
    )
    probability_U2 = DiscreteUnconditionalProbability.from_db_model(probability_U2)

    id_uncertainty_u1 = UncertaintyNode("u1", "U1", probabilities=probability_U1)
    id_uncertainty_u2 = UncertaintyNode("u2", "U2", probabilities=probability_U2)
    id_decision = DecisionNode("D", "D", alternatives=["green", "red"])

    id_e0 = Edge(id_uncertainty_u1, id_decision)
    id_e1 = Edge(id_uncertainty_u2, id_decision)

    net = {
        "nodes": [id_uncertainty_u1, id_uncertainty_u2, id_decision],
        "edges": [id_e0, id_e1],
    }

    ID = InfluenceDiagram()
    for node in net["nodes"]:
        ID.add_node(node)
    for edge in net["edges"]:
        ID.add_edge(edge)

    dt_uncertainty_u1 = UncertaintyNode("u1", "U1", probabilities=probability_U1)

    dt_uncertainty_u2_1 = UncertaintyNode("u2", "U2", probabilities=probability_U2)
    dt_e0 = Edge(dt_uncertainty_u1, dt_uncertainty_u2_1, name="high")
    dt_decision_1 = DecisionNode("D", "D", alternatives=["green", "red"])
    dt_e1 = Edge(dt_uncertainty_u2_1, dt_decision_1, name="yes")
    dt_utility_0 = UtilityNode("v", "Utility", utility=None)
    dt_e2 = Edge(dt_decision_1, dt_utility_0, name="green")
    dt_utility_1 = UtilityNode("v", "Utility", utility=None)
    dt_e3 = Edge(dt_decision_1, dt_utility_1, name="red")

    dt_decision_2 = DecisionNode("D", "D", alternatives=["green", "red"])
    dt_e4 = Edge(dt_uncertainty_u2_1, dt_decision_2, name="no")
    dt_utility_2 = UtilityNode("v", "Utility", utility=None)
    dt_e5 = Edge(dt_decision_2, dt_utility_2, name="green")
    dt_utility_3 = UtilityNode("v", "Utility", utility=None)
    dt_e6 = Edge(dt_decision_2, dt_utility_3, name="red")

    dt_uncertainty_u2_2 = UncertaintyNode("u2", "U2", probabilities=probability_U2)
    dt_e7 = Edge(dt_uncertainty_u1, dt_uncertainty_u2_2, name="low")
    dt_decision_3 = DecisionNode("D", "D", alternatives=["green", "red"])
    dt_e8 = Edge(dt_uncertainty_u2_2, dt_decision_3, name="yes")
    dt_utility_4 = UtilityNode("v", "Utility", utility=None)
    dt_e9 = Edge(dt_decision_3, dt_utility_4, name="green")
    dt_utility_5 = UtilityNode("v", "Utility", utility=None)
    dt_e10 = Edge(dt_decision_3, dt_utility_5, name="red")

    dt_decision_4 = DecisionNode("D", "D", alternatives=["green", "red"])
    dt_e11 = Edge(dt_uncertainty_u2_2, dt_decision_4, name="no")
    dt_utility_6 = UtilityNode("v", "Utility", utility=None)
    dt_e12 = Edge(dt_decision_4, dt_utility_6, name="green")
    dt_utility_7 = UtilityNode("v", "Utility", utility=None)
    dt_e13 = Edge(dt_decision_4, dt_utility_7, name="red")

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
        "edges": [
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
    for node in net["nodes"]:
        DT.add_node(node)
    for edge in net["edges"]:
        DT.add_edge(edge)

    IDT = ID.convert_to_decision_tree()
    for id_node, dt_node in zip(IDT.nx.nodes, DT.nx.nodes, strict=False):
        assert type(id_node) is type(dt_node)
        assert id_node.description == dt_node.description
        if not isinstance(id_node, UtilityNode):
            assert id_node.shortname == dt_node.shortname

    for id_edge, dt_edge in zip(IDT.nx.edges, DT.nx.edges, strict=False):
        assert type(id_edge) is type(dt_edge)
        assert id_edge[0].description == dt_edge[0].description
        assert id_edge[1].description == dt_edge[1].description
        assert (
            IDT.nx.edges[id_edge[0], id_edge[1]]["name"]
            == DT.nx.edges[dt_edge[0], dt_edge[1]]["name"]
        )
        assert (
            IDT.nx.edges[id_edge[0], id_edge[1]]["arc_type"]
            == DT.nx.edges[dt_edge[0], dt_edge[1]]["arc_type"]
        )


def test_to_pyagrum_used_car_buyer_success(copy_testdata_tmpdir, tmp_path):
    copy_testdata_tmpdir(TESTDATA)
    with open(tmp_path / "id_used_car_buyer.json") as f:
        json_stream = json.load(f)
    influence_diagram_response = InfluenceDiagramResponse(
        vertices=json_stream["vertices"], edges=json_stream["edges"]
    )
    ID = InfluenceDiagram.from_db(influence_diagram_response)

    result = ID.to_pyagrum()
    assert isinstance(result, gum.InfluenceDiagram)
    assert result.size() == 5
    assert result.chanceNodeSize() == 2
    assert result.decisionNodeSize() == 2
    assert result.utilityNodeSize() == 1

    # import pyAgrum.lib.image as gimg
    # from shutil import copyfile
    # gimg.export(result, "test2.png")
    # result.saveBIFXML("test.bifxml")
    # testroot = '/tmp/pytest-of-codespace/pytest-current/'
    # testpath = testroot+'test_to_pyagrum_used_car_buyercurrent/'
    # copyfile(testpath+"test2.png", "/workspaces/dot/test2.png")
    # copyfile(testpath+"test.bifxml", "/workspaces/dot/test.bifxml")


def test_to_pyagrum_used_car_buyer_not_acyclic_fail(
    caplog, copy_testdata_tmpdir, tmp_path
):
    copy_testdata_tmpdir(TESTDATA)
    with open(tmp_path / "id_used_car_buyer.json") as f:
        json_stream = json.load(f)
    influence_diagram_response = InfluenceDiagramResponse(
        vertices=json_stream["vertices"], edges=json_stream["edges"]
    )
    ID = InfluenceDiagram.from_db(influence_diagram_response)
    node0 = list(ID.nx.nodes)[0]
    node1 = list(ID.nx.nodes)[1]
    edge1 = Edge(node0, node1, name="cyclic")
    edge2 = Edge(node1, node0, name="cyclic")
    ID.add_edge(edge1)
    ID.add_edge(edge2)

    with pytest.raises(Exception) as exc_info:
        ID.to_pyagrum()
    assert [r.msg for r in caplog.records] == ["the influence diagram is not acyclic."]
    assert str(exc_info.value) == "the influence diagram is not acyclic."


def test_to_pyagrum_used_car_buyer_uncertainty_fail(
    caplog, copy_testdata_tmpdir, tmp_path
):
    copy_testdata_tmpdir(TESTDATA)
    with open(tmp_path / "id_used_car_buyer.json") as f:
        json_stream = json.load(f)
    influence_diagram_response = InfluenceDiagramResponse(
        vertices=json_stream["vertices"], edges=json_stream["edges"]
    )
    node_index = [
        k
        for k, node in enumerate(influence_diagram_response.vertices)
        if node.category == "Uncertainty"
    ][0]
    influence_diagram_response.vertices[node_index].probabilities = None
    ID = InfluenceDiagram.from_db(influence_diagram_response)

    error = (
        "[pyAgrum] Invalid argument: Empty variable State:Labelized({}) "
        "cannot be added in a Potential"
    )
    with pytest.raises(Exception) as exc_info:
        ID.to_pyagrum()
    assert [r.msg for r in caplog.records] == [
        f"Input probability cannot be used in pyagrum with error: {error}"
    ]
    assert (
        str(exc_info.value)
        == f"Input probability cannot be used in pyagrum with error: {error}"
    )


def test_to_pyagrum_used_car_buyer_decision_fail(caplog, copy_testdata_tmpdir, tmp_path):
    copy_testdata_tmpdir(TESTDATA)
    with open(tmp_path / "id_used_car_buyer.json") as f:
        json_stream = json.load(f)
    influence_diagram_response = InfluenceDiagramResponse(
        vertices=json_stream["vertices"], edges=json_stream["edges"]
    )
    node_index = [
        k
        for k, node in enumerate(influence_diagram_response.vertices)
        if node.category == "Decision"
    ][0]
    influence_diagram_response.vertices[node_index].alternatives = None
    ID = InfluenceDiagram.from_db(influence_diagram_response)

    error = (
        "[pyAgrum] Invalid argument: Empty variable Buy:Labelized({}) "
        "cannot be added in a Potential"
    )
    with pytest.raises(Exception) as exc_info:
        ID.to_pyagrum()
    assert [r.msg for r in caplog.records] == [
        f"Input arc cannot be used in pyagrum with error: {error}"
    ]
    assert (
        str(exc_info.value) == f"Input arc cannot be used in pyagrum with error: {error}"
    )

    # def test_convert_to_decision_tree_asymemetry():


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
