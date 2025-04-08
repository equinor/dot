import numpy as np

from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)
from src.v0.services.classes.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
)


def test_class_DecisionNode():
    node = DecisionNode(description="junk", shortname="J")
    assert node.description == "junk"
    assert node.shortname == "J"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert isinstance(node.alternatives, list) and not node.alternatives
    assert isinstance(node.states, list) and not node.states
    assert node.is_decision_node
    assert not node.is_uncertainty_node
    assert not node.is_utility_node


def test_class_DecisionNode_setter_alternatives_as_list():
    node = DecisionNode(description="junk", shortname="J")
    node.description = "C2H5OH"
    node.shortname = "ethanol"
    node.uuid = None
    node.alternatives = ["1", "2", "3"]
    assert node.description == "C2H5OH"
    assert node.shortname == "ethanol"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert node.alternatives == ["1", "2", "3"]


def test_class_DecisionNode_setter_alternatives_as_empty():
    node = DecisionNode(description="junk", shortname="J")
    node.description = "C2H5OH"
    node.shortname = "ethanol"
    node.uuid = None
    node.alternatives = []
    assert node.description == "C2H5OH"
    assert node.shortname == "ethanol"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert node.alternatives == []


def test_class_DecisionNode_setter_alternatives_as_tuple():
    node = DecisionNode(description="junk", shortname="J")
    node.description = "C2H5OH"
    node.shortname = "ethanol"
    node.uuid = None
    node.alternatives = ("1", "2", "3")
    assert node.description == "C2H5OH"
    assert node.shortname == "ethanol"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert node.alternatives == ["1", "2", "3"]


def test_class_UncertaintyNode():
    node = UncertaintyNode(description="junk", shortname="J")
    assert node.description == "junk"
    assert node.shortname == "J"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert node.probability is None
    assert isinstance(node.outcomes, tuple) and not node.outcomes
    assert isinstance(node.states, tuple) and not node.states
    assert not node.is_decision_node
    assert node.is_uncertainty_node
    assert not node.is_utility_node


def test_class_UncertaintyNode_setter():
    node = UncertaintyNode(description="junk", shortname="J")
    node.probability = DiscreteUnconditionalProbability(
        probability_function=np.array([1, 0]), variables={"outcome": ["y", "n"]}
    )
    assert node.outcomes == ("y", "n")


def test_class_UtilityNode():
    node = UtilityNode(description="junk", shortname="J")
    assert node.description == "junk"
    assert node.shortname == "J"
    assert isinstance(node.uuid, str)
    assert len(node.uuid) == 36
    assert node.states == []
    assert not node.is_decision_node
    assert not node.is_uncertainty_node
    assert node.is_utility_node
    node.utility = []
    assert node.states == []


def test_class_UtilityNode_setter():
    node = UtilityNode(description="junk", shortname="J")
    assert isinstance(node, UtilityNode)


def test_copy():
    node = DecisionNode(
        description="junk", shortname="J", alternatives=["a0", "a1", "a2"]
    )
    copied_node = node.copy()
    assert isinstance(copied_node, type(node))
    assert copied_node.description == node.description
    assert copied_node.shortname == node.shortname
    assert copied_node.alternatives == node.alternatives
