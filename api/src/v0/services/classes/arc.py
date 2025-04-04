"""Arc classes

    Raises:
        EndpointTypeError: When endpoint cannot be set to start or end
        UtilityNodeSuccessorError: When a UtilityNode has a successor which
        is not another UtilityNode
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from src.v0.services.classes.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
    )

if TYPE_CHECKING:  # pragma: no cover
    from src.v0.services.classes.node import NodeABC

from .errors import UtilityNodeSuccessorError
from .validations import validate_and_set_arc


class Arc:
    """Class of arcs"""

    def __init__(
        self,
        *,
        tail: NodeABC,
        head: NodeABC,
        label: str = None,
        unique_id=None
        ):
        """Instance of Arc

        Args:
            tail (NodeABC): start node of the arc
            head (NodeABC): end node of the arc
            label (str, optional): label of the arc. Defaults to None.
            unique_id (str, optional): uuid. Defaults to None. If None,
            the uuid is attributed at instantiation.

        Private attributes:
            _tail (NodeABC): start node of the arc
            _head (NodeABC): end node of the arc
            _label (str, optional): label of the arc. Defaults to None.
            _uuid (str, optional): uuid. Defaults to None. If None, the uuid
            is attributed at instantiation.
        """
        self._tail = validate_and_set_arc.edge(tail)
        self._head = validate_and_set_arc.edge(head)
        self._label = validate_and_set_arc.label(label)
        self._uuid = validate_and_set_arc.uuid(unique_id)

    @property
    def tail(self) -> NodeABC:
        """
        Returns:
            NodeABC: the node at start of the arc (tail)
        """
        return self._tail

    @property
    def head(self) -> NodeABC:
        """
        Returns:
            NodeABC: the node at end of the arc (head)
        """
        return self._head

    @property
    def label(self) -> str:
        """
        Returns:
            str: the label of the arc
        """
        return self._label

    @property
    def uuid(self) -> str:
        """Return the `uuid` attribute

        Returns:
            str: uuid of the node
        """
        return self._uuid

    @property
    def dtype(self):
        """type of the arc (informational/conditional)"""
        if isinstance(self.head, DecisionNode):
            return "informational"
        elif isinstance(self.head, UncertaintyNode):
            return "conditional"
        elif isinstance(self.head, UtilityNode):
            return "functional"
        elif self.head is None:
            return None

    @label.setter
    def label(self, value):
        self._label = validate_and_set_arc.label(value)

    @tail.setter
    def tail(self, node):
        if node.is_utility_node:
            if not (self.head.is_utility_node or self.head is None):
                raise UtilityNodeSuccessorError(f"{self.head.uuid}/{node.uuid}")
        self._tail = validate_and_set_arc.edge(node)

    @head.setter
    def head(self, node):
        if self.tail.is_utility_node and not node.is_utility_node:
            raise UtilityNodeSuccessorError(f"{self.tail.uuid}/{node.uuid}")
        self._head = validate_and_set_arc.edge(node)

    def copy(self):
        """copy an arc

        Returns:
            Arc: copied arc, endpoints keeping their uuids
        """
        # need to create the arc and then fill it so that
        # the endpoints are the same including uuid
        arc = Arc(tail=None, head=None, label=self.label)
        arc.tail = self.tail
        arc.head = self.head
        return arc
