"""Module defining the InfluenceDiagram class

An InfluenceDiagram is a sub-class of DirectedGraphABC.
"""

from src.v0.services.classes.node import (
    DecisionNode,
    UncertaintyNode,
    UtilityNode,
)

from .abstract_directed_graph import DirectedGraphABC


class InfluenceDiagram(DirectedGraphABC):
    """Influence Diagram"""

    def __init__(self):
        """
        Create an instance of an InfluenceDiagram
        It is a wrapper around networkx.Digraph

        Attributes:
            graph (networkx.DiGraph): networkx.DiGraph object
            containing the influence diagram (nodes and arcs)
        """
        super().__init__()

    def get_decision_nodes(self) -> list[DecisionNode]:
        """Return a list of decision nodes

        Returns:
            list[DecisionNode]
        """
        return [
            node[0]
            for node in list(self.graph.nodes(data=True))
            if isinstance(node[0], DecisionNode)
        ]

    def get_uncertainty_nodes(self) -> list[UncertaintyNode]:
        """Return a list of uncertainty nodes

        Returns:
            list[UncertaintyNode]
        """
        return [
            node[0]
            for node in list(self.graph.nodes(data=True))
            if isinstance(node[0], UncertaintyNode)
        ]

    def get_utility_nodes(self) -> list[UtilityNode]:
        """Return a list of utility nodes

        Returns:
            list[UtilityNode]
        """
        return [
            node[0]
            for node in list(self.graph.nodes(data=True))
            if isinstance(node[0], UtilityNode)
        ]

    @property
    def decision_count(self) -> int:
        """Return the number of decision nodes

        Returns:
            int: the number of DecisionNode objects in the influence diagram
        """
        return len(self.get_decision_nodes())

    @property
    def uncertainty_count(self) -> int:
        """Return the number of uncertainty nodes

        Returns:
            int: the number of UncertaintyNode objects in the influence diagram
        """
        return len(self.get_uncertainty_nodes())

    @property
    def utility_count(self) -> int:
        """Return the number of utility nodes

        Returns:
            int:  the number of UtilityNode objects in the influence diagram
        """
        return len(self.get_utility_nodes())
