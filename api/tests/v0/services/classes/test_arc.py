from unittest.mock import MagicMock

import pytest
from src.v0.services.classes.arc import Arc
from src.v0.services.classes.node import (DecisionNode, UncertaintyNode,
                                       UtilityNode)
from src.v0.services.structure_utils.decision_diagrams.influence_diagram import InfluenceDiagram


def test_class_InformationalArc():
    n1 = UncertaintyNode(description="junk", shortname="J")
    n2 = DecisionNode(description="junky", shortname="H")
    arc = Arc(tail=n1, head=n2, label="first")
    assert arc.tail == n1
    assert arc.head == n2
    assert arc.label == "first"
    assert arc.dtype == "informational"


def test_class_InformationalArc_without_name():
    n1 = UncertaintyNode(description="junk", shortname="J")
    n2 = DecisionNode(description="junky", shortname="H")
    arc = Arc(tail=n1, head=n2)
    assert arc.label is None


def test_class_set_name():
    n1 = UncertaintyNode(description="junk", shortname="J")
    n2 = DecisionNode(description="junky", shortname="H")
    arc = Arc(tail=n1, head=n2)
    arc.label = "C2H5OH"
    assert arc.label == "C2H5OH"


def test_class_ConditionalArc():
    n1 = UncertaintyNode(description="junk", shortname="J")
    n2 = UncertaintyNode(description="junky", shortname="H")
    arc = Arc(tail=n1, head=n2, label="second")
    assert arc.tail.description == "junk"
    assert arc.tail.shortname == "J"
    assert arc.head.description == "junky"
    assert arc.head.shortname == "H"
    assert arc.label == "second"
    assert arc.dtype == "conditional"


def test_class_FunctionalArc():
    n1 = UncertaintyNode(description="junk", shortname="J")
    n2 = UtilityNode(description="junky", shortname="H")
    arc = Arc(tail=n1, head=n2, label="first")
    assert arc.tail == n1
    assert arc.head == n2
    assert arc.label == "first"
    assert arc.dtype == "functional"


def test_copy():
    n1 = UncertaintyNode(description="junk", shortname="J")
    n2 = DecisionNode(description="junky", shortname="H")
    arc = Arc(tail=n1, head=n2, label="first")
    copied_arc = arc.copy()
    assert copied_arc.tail == arc.tail
    assert copied_arc.head == arc.head
    assert copied_arc.label == arc.label


def test_set_head():
    n1 = UncertaintyNode(description="junk", shortname="J")
    n2 = DecisionNode(description="junky", shortname="H")
    arc = Arc(tail=n1, head=None, label="first")
    assert arc.tail == n1
    assert arc.head is None
    assert arc.label == "first"
    assert arc.dtype is None
    arc.head = n2
    assert arc.head == n2
    assert arc.dtype == "informational"


def test_set_head_fail(caplog):
    n1 = UtilityNode(description="junk", shortname="J", uuid="775e46e5-2dd4-4e34-add6-bb8c0626627d")
    n2 = DecisionNode(description="junky", shortname="H", uuid="66095d54-74dc-4a75-bcf4-49676a44a2a2")
    arc = Arc(tail=n1, head=None, label="first")
    with pytest.raises(Exception) as exc_info:
        arc.head = n2
    assert [r.msg for r in caplog.records] == [(
        "Utility node can only have other utility nodes as successor: "
        "775e46e5-2dd4-4e34-add6-bb8c0626627d/66095d54-74dc-4a75-bcf4-49676a44a2a2"
        )]
    assert str(exc_info.value) == (
        "Utility node can only have other utility nodes as successor: "
        "775e46e5-2dd4-4e34-add6-bb8c0626627d/66095d54-74dc-4a75-bcf4-49676a44a2a2"
        )


def test_set_tail():
    n1 = UncertaintyNode(description="junk", shortname="J")
    n2 = DecisionNode(description="junky", shortname="H")
    arc = Arc(tail=None, head=n2, label="first")
    assert arc.tail is None
    assert arc.head == n2
    assert arc.label == "first"
    assert arc.dtype == "informational"
    arc.tail = n1
    assert arc.tail == n1
    assert arc.dtype == "informational"


def test_set_tail_fail(caplog):
    n1 = UtilityNode(description="junk", shortname="J", uuid="775e46e5-2dd4-4e34-add6-bb8c0626627d")
    n2 = DecisionNode(description="junky", shortname="H", uuid="66095d54-74dc-4a75-bcf4-49676a44a2a2")
    arc = Arc(tail=None, head=n2, label="first")
    with pytest.raises(Exception) as exc_info:
        arc.tail = n1
    assert [r.msg for r in caplog.records] == [(
        "Utility node can only have other utility nodes as successor: "
        "66095d54-74dc-4a75-bcf4-49676a44a2a2/775e46e5-2dd4-4e34-add6-bb8c0626627d"
        )]
    assert str(exc_info.value) == (
        "Utility node can only have other utility nodes as successor: "
        "66095d54-74dc-4a75-bcf4-49676a44a2a2/775e46e5-2dd4-4e34-add6-bb8c0626627d"
        )