"""Module defining the ProbabilisticGraphModel Abstract class
"""

from __future__ import annotations

from abc import ABC
from collections.abc import Sequence
from typing import TYPE_CHECKING

import networkx as nx

from .arc import Arc
from .errors import NodeInGraphError
from .validations import validate_and_set_graph_model

if TYPE_CHECKING:  # pragma: no cover
    from .node import NodeABC


class DirectedGraphType:
    @staticmethod
    def get_validation_node_method(self):
        if type(self).__qualname__ == "InfluenceDiagram":
            method = "id_node"
        elif type(self).__qualname__ == "DecisionTree":
            method = "dt_node"
        return getattr(validate_and_set_graph_model, method)


class DirectedGraphABC(ABC):

    NODES_MODULE_PATH = "src.v0.services.classes.node"

    """Directed  Graph

    While nodes are unique in the graph, it may exist several relationship
    between them, expressed as the possibility to have several arcs between
    two given nodes.
    """

    def __init__(self):
        """
        Create an instance of a DirectedGraphABC (ABSTRACT class!!!)
        It is a wrapper around networkx.Digraph

        Attributes:
            graph: networkx object
        """
        self.graph = nx.DiGraph()

    @property
    def is_acyclic(self) -> bool:
        """test if the graph is acyclic or not.

        An influence diagram or a decision tree are acyclic. However, during
        the building process, the condition may not be true.

        Returns:
            bool: True if the graph is acyclic, False otherwise.
        """
        return nx.is_directed_acyclic_graph(self.graph)

    @property
    def nodes(self) -> list[NodeABC]:
        """List of the graph nodes

        Returns:
            List[NodeABC]: the list of node instances
        """
        return list(self.graph.nodes)

    @property
    def arcs(self) -> list[Arc]:
        """List of the graph arcs

        Returns:
            List[Arc]: the list of arc instances
        """
        g = nx.node_link_data(self.graph, source="tail", target="head", link="edges")
        return [
            Arc(
                tail=item["tail"],
                head=item["head"],
                label=item["label"],
                unique_id=item["uuid"]
                ) for item in g["edges"]
            ]

    @property
    def node_uuids(self) -> list:
        """List of uuid's of the graph nodes

        Returns:
            List: the list of uuid's
        """
        return [node.uuid for node in self.graph]

    def node_in(self, node: NodeABC) -> bool:
        """Check if a node is in the graph.

        The test is done through the uuid of the nodes.

        Args:
            node (NodeABC): the node to be tested

        Returns:
            bool: True if the node is already within the graph, False otherwise.
        """
        return node.uuid in self.node_uuids

    def add_nodes(self, nodes: Sequence[NodeABC]):
        """Add a list/tuple of nodes to a graph

        Args:
            nodes (Sequence[NodeABC]): list/tuple of the nodes to be added
        """
        for node in nodes:
            self.add_node(node)

    def add_arcs(self, arcs: Sequence[Arc]):
        """Add a list/tuple of arcs to a graph.
            Endpoints of the arcs which are not already in the graph are added.

        Args:
            arcs (Sequence[Arcs]): list/tuple of the arcs to be added
        """
        for arc in arcs:
            self.add_arc(arc)

    def add_node(self, node: NodeABC):
        """Add a node to the graph

        Args:
            node (NodeABC): node to be added
        """
        validation_method = DirectedGraphType.get_validation_node_method(self)
        if not self.node_in(node):
            self.graph.add_node(validation_method(node))

    def add_arc(self, arc: Arc):
        """Add an arc to the graph

        Args:
            arc (Arc): arc to be added. If some of the end points do not exist,
            they are added to the graph too.
        """
        arc_info = validate_and_set_graph_model.arc_to_graph(arc)
        tail = arc_info[0][0] if not self.node_in(arc_info[0][0]) \
            else self.get_node_from_uuid(arc_info[0][0].uuid)
        head = arc_info[0][1] if not self.node_in(arc_info[0][1]) \
            else self.get_node_from_uuid(arc_info[0][1].uuid)
        self.graph.add_edge(tail, head, **arc_info[1])

    def copy(self):
        """copy the probabilistic graph model

        Returns
            ProbabilisticGraphModel: a copy of the graph. uuid's of
            the nodes are copied too.
        """
        new_graph = type(self)()  # Need to instance from the concrete class
        new_graph.graph = self.graph.copy()
        return new_graph

    def get_parents(self, node: NodeABC) -> list[NodeABC]:
        """get parents of a given node

        Args:
            node (NodeABC): node to find the parents of

        Returns
            List[NodeABC]: the list of the parents of the given node
        """
        if not self.graph.has_node(node):
            raise NodeInGraphError(node)
        return list(self.graph.predecessors(node))

    def get_children(self, node: NodeABC) -> list[NodeABC]:
        """get children of a given node

        Args:
            node (NodeABC): node to find the children of

        Returns
            List[NodeABC]: the list of the children of the given node
        """
        if not self.graph.has_node(node):
            raise NodeInGraphError(node)
        return list(self.graph.successors(node))

    def has_children(self, node: NodeABC) -> bool:
        """Check for existence of children

        Args:
            node (NodeABC): node to check for children

        Returns
            bool: existence (True) or not (False) of children to the given node
        """
        return len(self.get_children(node)) > 0

    def get_node_from_uuid(self, uuid: str) -> NodeABC:
        """get a node given its uuid

        Args:
            uuid (str): uuid of node to look for

        Returns:
            NodeABC: node object having the given uuid
        """
        return [node for node in self.graph if node.uuid == uuid][0]

    # def get_node_type(self, node: NodeABC) -> str:
    #     """Return the type of a given node

    #     Args:
    #         node (NodeABC): node to examine

    #     Returns
    #         str: a string describing the type of the node (class name in
    #         lower font and without the "Node" suffix)
    #     """
    #     return type(node).__name__.replace("Node", "").lower()
