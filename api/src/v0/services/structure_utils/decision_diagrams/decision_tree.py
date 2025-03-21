"""Module defining the DecisionTree class

A DecisionTree is a sub-class of ProbabilisticGraphModel.

    Raises:
        RootNodeNotFound: When trying to define a decision tree without giving the root
                          node

"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import networkx as nx

from ..decision_diagrams.probabilistic_graph_model import ProbabilisticGraphModelABC

if TYPE_CHECKING:  # pragma: no cover
    from ..decision_diagrams.node import NodeABC


logger = logging.getLogger(__name__)


class RootNodeNotFound(Exception):
    def __init__(self):
        error_message = "Decision tree has no defined root node"
        super().__init__(error_message)
        logger.critical(error_message)


class DecisionTree(ProbabilisticGraphModelABC):
    """Decision tree class"""

    def __init__(self, *args, **kwargs):
        """Create an instance of a DecisionTree
            It is a wrapper around networkx.Digraph

        Args:
            *args, **kwargs: arguments for networkx.DiGraph

        Attributes:
            nx (networkx.DiGraph): networkx.DiGraph object containing the decision tree
                                  (nodes and arcs)
        """
        super().__init__(*args, **kwargs)
        self.root = kwargs.get("root", None)
        if self.root is not None:
            self.nx.add_node(self.root)

    @classmethod
    def initialize_diagram(cls, data: dict):
        """Initialize a DecisionTree from data

        It looks for the node without parent for setting it
        first in the list of nodes

        Args:
            data (Dict): dictionary describing the graph model
                {"nodes": List[NodeABC], "edges": List[Edge]}

            Only the 'edges' attribute is actually used.

        Returns:
            DecisionTree: a new DecisionTree instance

        Example:
            >>> n0 = UncertaintyNode("Uncertainty node 0", "u0")
            >>> n1 = UncertaintyNode("Uncertainty node 1", "u1")
            >>> n2 = UncertaintyNode("Uncertainty node 2", "u2")
            >>> n3 = DecisionNode("Decision node 0", "d0")
            >>> n4 = DecisionNode("Decision node 1", "d1")
            >>> n5 = DecisionNode("Decision node 2", "d2")
            >>> e0 = Edge(n0, n1, name="e0")
            >>> e1 = Edge(n0, n2, name="e1")
            >>> e2 = Edge(n1, n3, name="e2")
            >>> e3 = Edge(n1, n4, name="e3")
            >>> e4 = Edge(n2, n5, name="e2")
            >>> graph = {"nodes": [n0, n1, n2, n3, n4, n5], \
            ...  "edges": [e0, e1, e2, e3, e4],}
            >>> DecisionTree.initialize_diagram(graph)
        """
        roots = []
        g = nx.DiGraph([(arc.endpoint_start, arc.endpoint_end) for arc in data["edges"]])
        roots = [node for node in g.nodes if not list(g.predecessors(node))]
        if not len(roots) == 1:
            raise RootNodeNotFound
        return cls(root=roots[0])

    def set_root(self, root: NodeABC):
        """set the root to a DecisionTree when this one has not been given
            Typically, used if an empty decision tree is first generated and
            then a node is given as its root.

        Args:
            root (NodeABC): the root node
        """
        self.root = root
        if not self.nx.has_node(root):
            self.add_node(root)

    def parent(self, node: NodeABC) -> NodeABC | None:
        """return the parent node in the Decition Tree

        In a Decision Tree, a node has a unique parent
        (The root doesn't have any)

        Args:
            node (NodeABC): node to find the parent of

        Returns
            Union[NodeABC, None]: the parent node or None is no parent node has been
                                  found
        """
        parents = self.get_parents(node)
        return parents[0] if len(parents) > 0 else None

    def _to_json_stream(self) -> dict:
        """convert the decision tree instance into a dictionary
            It uses the method `networkx.readwrite.json_graph.tree_data()`

        Raises:
            RootNodeNotFound: Raised when no root has been set in the decision tree

        Returns:
            Dict: a representation of the tree
        """

        def propagate_branch_name(self, node, names):
            predecessor = self.parent(node)
            if not predecessor:
                return ""
            n = names[(predecessor, node)]
            return n if isinstance(n, str) else "-".join(n)

        if self.root is None:
            raise RootNodeNotFound

        edges_name = nx.get_edge_attributes(self.nx, "name")
        tg = nx.readwrite.json_graph.tree_data(self.nx, self.root)
        json_object = json.dumps(
            tg,
            default=lambda o: {
                **o.to_dict(),
                **{"branch_name": propagate_branch_name(self, o, edges_name)},
            },
            indent=2,
        )
        return json_object
