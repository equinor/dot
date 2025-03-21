"""Edges classes

Raises:
    EndpointTypeError: When endpoint cannot be set to start or end
    UtilityNodeSuccessorError: When a UtilityNode has a successor which is not another
                               UtilityNode
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from ..decision_diagrams.node import DecisionNode, UncertaintyNode, UtilityNode

if TYPE_CHECKING:  # pragma: no cover
    from ....models.edge import EdgeResponse
    from ..decision_diagrams.node import NodeABC
    from ..decision_diagrams.probabilistic_graph_model import ProbabilisticGraphModelABC


logger = logging.getLogger(__name__)


class EndpointTypeError(Exception):
    def __init__(self, mode):
        self.mode = mode
        error_message = f"endpoint cannot be set to mode {mode}"
        super().__init__(error_message)
        logger.critical(error_message)


class UtilityNodeSuccessorError(Exception):
    def __init__(self):
        error_message = "utility node can only have other utility nodes as successor"
        super().__init__(error_message)
        logger.critical(error_message)


class Edge:
    """Class of nodes"""

    def __init__(
        self,
        endpoint_start: NodeABC,
        endpoint_end: NodeABC,
        name: str = None,
        **kwargs,
    ):
        """Instance of Edge

        Args:
            endpoint_start (NodeABC): start node of the edge
            endpoint_end (NodeABC): end node of the edge
            name (str, optional): name of the edge. Defaults to None.

        Private attributes:
            _endpoint_start (NodeABC): start node of the edge
            _endpoint_end (NodeABC): end node of the edge
            _name (str, optional): name of the edge. Defaults to None.
            _arc_type (str): type of the arc/edge, depending on the head node

        """
        self._endpoint_start = endpoint_start
        self._endpoint_end = endpoint_end
        self._name = name
        self._arc_type = None
        self._set_arc_type()

    @classmethod
    def from_dict(cls, edge: dict, pgm: ProbabilisticGraphModelABC):
        """Create an Edge instance from dictionary information

        endpoint nodes need to have already been added to the graph

        Args
            edge (Dict): description of the edage as dictionary.
                    'from' the uuid of the start endpoint of the edge (tail)
                    'to' the uuid of the end endpoint of the edge (head)
                    'name' the name of the edge
            pgm (ProbabilisticGraphModel): the diagram into which the edge is added.
                                           This is only used to get the nodes from
                                           their uuid's.

        Returns:
            Edge: a new edge instance is created.

        :warning: The Edge is not added to the diagram !!!
        """
        endpoint_start = pgm.get_node_from_uuid(edge["from"])
        endpoint_end = pgm.get_node_from_uuid(edge["to"])
        attributes = {k: v for k, v in edge.items() if k not in ["from", "to", "id"]}
        return cls(endpoint_start, endpoint_end, attributes.get("name", None))

    @property
    def endpoint_start(self) -> NodeABC:
        """
        Returns:
            NodeABC: the node at start of the edge (tail)
        """
        return self._endpoint_start

    @property
    def endpoint_end(self) -> NodeABC:
        """
        Returns:
            NodeABC: the node at end of the edge (head)
        """
        return self._endpoint_end

    @property
    def name(self) -> str:
        """
        Returns:
            str: the name of the edge
        """
        return self._name

    def copy(self):
        """copy an edge

        Returns:
            Edge: copied edge, endpoints keeping their uuids
        """
        # need to create the edge and then fill it so that
        # the endpoints are the same including uuid
        edge = Edge(None, None, self.name)
        edge.set_endpoint(self.endpoint_start, mode="start")
        edge.set_endpoint(self.endpoint_end, mode="end")
        return edge

    def _set_arc_type(self):
        """set (if possible) the type of the arc/edge (informational/conditional)"""
        if isinstance(self._endpoint_end, DecisionNode):
            self._arc_type = "informational"
        elif isinstance(self._endpoint_end, UncertaintyNode):
            self._arc_type = "conditional"
        elif isinstance(self._endpoint_end, UtilityNode):
            self._arc_type = "functional"

    def set_endpoint(self, node: NodeABC, mode="end"):
        """Add an endpoint to an edge

            When creating an Edge, it does not need to have endpoints. Those endpoints
            can be added at a later stage. This is actually necessary when converting an
            influence diagram to a decision tree.

        Args:
            node (NodeABC): node to add as an endpoint
            mode (str, optional): where to add the node ['start'|'end'].
                                  Defaults to "end".

        Raises:
            EndpointTypeError: _description_
            UtilityNodeSuccessorError: _description_
        """
        if mode == "end":
            self._endpoint_end = node
        elif mode == "start":
            self._endpoint_start = node
        else:
            raise EndpointTypeError(mode)
        if mode == "end" and self._endpoint_start.is_utility_node:
            if not node.is_utility_node:
                raise UtilityNodeSuccessorError

        self._set_arc_type()

    def to_nx(self) -> tuple[tuple[NodeABC, NodeABC], dict]:
        """convert the edge to a format compatible with the networkx format

        Returns:
            Tuple[Tuple[NodeABC, NodeABC], Dict]: The Tuple[NodeABC, NodeABC] represents
                                                  the edge itself, and the Dictionary
                                                  adds extra information to the edge.
        """
        return (self._endpoint_start, self._endpoint_end), {
            "arc_type": self._arc_type,
            "name": self._name,
        }

    @classmethod
    def from_db(cls, response: EdgeResponse, nodes: list[NodeABC]):
        """create an Edges defined as an EdgeResponse and given a list of NodeABC

        Args:
            response (EdgeResponse): response from DataBase defining the edge
            nodes (list[NodeABC]): nodes existing in the diagram

        Returns
            Edge: An Edge between existing nodes (NodeABC)
        """
        uuid_tail = response.outV
        uuid_head = response.inV
        tail = [node for node in nodes if node.uuid == uuid_tail][0]
        head = [node for node in nodes if node.uuid == uuid_head][0]
        return Edge(tail, head, **response.__dict__)
