import pytest

from src.v0.services.class_validations import validate_and_set_graph_model
from src.v0.services.classes.arc import Arc
from src.v0.services.classes.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
)


def test_id_node_success():
    assert validate_and_set_graph_model.id_node(
        DecisionNode(description="description", shortname="D")
    )
    assert validate_and_set_graph_model.id_node(
        UncertaintyNode(description="description", shortname="C")
    )
    assert validate_and_set_graph_model.id_node(
        UtilityNode(description="description", shortname="V")
    )


def test_id_fail(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_graph_model.id_node(None)
    assert [r.msg for r in caplog.records] == [
        (
            "Added node is not of instance "
            "(DecisionNode, UncertaintyNode, UtilityNode): None"
        )
    ]
    assert str(exc_info.value) == (
        "Added node is not of instance "
        "(DecisionNode, UncertaintyNode, UtilityNode): None"
    )


def test_dt_node_success():
    assert validate_and_set_graph_model.dt_node(
        DecisionNode(description="description", shortname="D")
    )
    assert validate_and_set_graph_model.dt_node(
        UncertaintyNode(description="description", shortname="C")
    )
    assert validate_and_set_graph_model.dt_node(
        UtilityNode(description="description", shortname="V")
    )


def test_dt_fail(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_graph_model.dt_node(None)
    assert [r.msg for r in caplog.records] == [
        (
            "Added node is not of instance "
            "(DecisionNode, UncertaintyNode, UtilityNode): None"
        )
    ]
    assert str(exc_info.value) == (
        "Added node is not of instance "
        "(DecisionNode, UncertaintyNode, UtilityNode): None"
    )


def test_arc_to_graph_success():
    n1 = UncertaintyNode(description="description", shortname="n1")
    n2 = DecisionNode(description="description", shortname="n2")
    arc = Arc(tail=n1, head=n2, label="arc_label")
    assert validate_and_set_graph_model.arc_to_graph(arc) == (
        (n1, n2),
        {"dtype": "informational", "label": "arc_label", "uuid": arc.uuid},
    )


def test_arc_to_graph_fail(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_graph_model.arc_to_graph(None)
    assert [r.msg for r in caplog.records] == ["Added arc is not of instance Arc: None"]
    assert str(exc_info.value) == "Added arc is not of instance Arc: None"
