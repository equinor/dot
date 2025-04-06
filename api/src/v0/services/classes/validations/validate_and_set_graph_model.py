from typing import Any

from src.v0.services.classes.arc import Arc
from src.v0.services.classes.node import (
    DecisionNode,
    NodeABC,
    UncertaintyNode,
    UtilityNode,
)

from ..errors import (
    ArcTypeValidationError,
    DTNodeTypeValidationError,
    IDNodeTypeValidationError,
)


def id_node(arg: Any) -> DecisionNode | UncertaintyNode | UtilityNode:
    if not isinstance(arg, DecisionNode | UncertaintyNode | UtilityNode):
        raise IDNodeTypeValidationError(arg)
    return arg


def dt_node(arg: Any) -> DecisionNode | UncertaintyNode | UtilityNode:
    if not isinstance(arg, DecisionNode | UncertaintyNode | UtilityNode):
        raise DTNodeTypeValidationError(arg)
    return arg


def arc_to_graph(arg: Any) -> tuple[tuple[NodeABC, NodeABC], dict]:
    if not isinstance(arg, Arc):
        raise ArcTypeValidationError(arg)
    return (arg.tail, arg.head), {
        "type": arg.dtype,
        "label": arg.label,
        "uuid": arg.uuid,
    }
