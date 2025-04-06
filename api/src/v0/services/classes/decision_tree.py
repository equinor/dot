"""Module defining the DecisionTree class

A DecisionTree is a sub-class of DirectedGraphABC.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from .abstract_directed_graph import DirectedGraphABC
from .validations import validate_and_set_graph_model

if TYPE_CHECKING:  # pragma: no cover
    from src.v0.services.classes.node import NodeABC


class DecisionTree(DirectedGraphABC):
    """Decision tree class"""

    def __init__(self, root: NodeABC = None):
        """Create an instance of a DecisionTree
            It is a wrapper around networkx.Digraph

        Attributes:
            graph (networkx.DiGraph): networkx.DiGraph object containing the
            decision tree (nodes and arcs)
        """
        super().__init__()
        if root is not None:
            self.add_node(validate_and_set_graph_model.dt_node(root))

    @property
    def root(self):
        """return the root node of the graph (no incoming arcs)

        Returns:
            NodeABC | None : the root node in the graph or None if none (cyclic) or
            more than 1 (graph under construction)
        """
        root_node = [n for n, d in self.graph.in_degree() if d == 0]
        if len(root_node) != 1:
            return None
        return root_node[0]

    def parent(self, node: NodeABC) -> NodeABC | None:
        """return the parent node in the Decition Tree

        In a Decision Tree, a node has a unique parent
        (The root doesn't have any)

        Args:
            node (NodeABC): node to find the parent of

        Returns
            NodeABC | None: the parent node or None is no parent node has been found
        """
        parents = self.get_parents(node)
        return parents[0] if len(parents) > 0 else None
