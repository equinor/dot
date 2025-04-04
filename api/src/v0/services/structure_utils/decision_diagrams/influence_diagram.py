"""Module defining the InfluenceDiagram class

An InfluenceDiagram is a sub-class of ProbabilisticGraphModel.

    Raises:
        PartialOrderOutputModeError: When input to the partial_order method is wrong

"""

from __future__ import annotations

import json
import logging
from typing import TYPE_CHECKING

import networkx as nx
import pyAgrum as gum

from ..decision_diagrams.decision_tree import DecisionTree
from ..decision_diagrams.edge import Edge
from ..decision_diagrams.node import DecisionNode, NodeABC, UncertaintyNode, UtilityNode
from ..decision_diagrams.probabilistic_graph_model import ProbabilisticGraphModelABC

if TYPE_CHECKING:  # pragma: no cover
    from ....models.structure import InfluenceDiagramResponse


logger = logging.getLogger(__name__)


class PartialOrderOutputModeError(Exception):
    def __init__(self, mode):
        self.mode = mode
        error_message = (
            f"output mode should be [view|copy] and have been entered as {mode}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class InfluenceDiagramNotAcyclicError(Exception):
    def __init__(self):
        error_message = "the influence diagram is not acyclic."
        super().__init__(error_message)
        logger.critical(error_message)


class ProbabilityFormatError(Exception):
    def __init__(self, error):
        self.mode = error
        error_message = (
            f"Input probability cannot be used in pyagrum with error: {error}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class ArcFormatError(Exception):
    def __init__(self, error):
        self.mode = error
        error_message = f"Input arc cannot be used in pyagrum with error: {error}"
        super().__init__(error_message)
        logger.critical(error_message)


class InfluenceDiagram(ProbabilisticGraphModelABC):
    """Influence Diagram"""

    def __init__(self, *args, **kwargs):
        """
        Create an instance of an InfluenceDiagram
        It is a wrapper around networkx.Digraph

        Args:
            *args, **kwargs: arguments for networkx.DiGraph

        Attributes:
            nx (networkx.DiGraph): networkx.DiGraph object containing
                                   the influence diagram (nodes and arcs)
        """
        super().__init__(*args, **kwargs)

    @classmethod
    def initialize_diagram(cls, data: dict):
        """initialize an influence diagram given nodes and edges in a dictionary

        Args:
            data (Dict): dictionary describing the graph model
                {"nodes": List[NodeABC], "edges": List[Edge]}

        Example:
            >>> n0 = UncertaintyNode("Uncertainty node 0", "u0")
            >>> n1 = UncertaintyNode("Uncertainty node 1", "u1")
            >>> n2 = DecisionNode("Decision node 0", "d0")
            >>> n3 = UncertaintyNode("Uncertainty node 2", "u2")
            >>> e0 = Edge(n0, n2, name="e0")
            >>> e1 = Edge(n1, n2, name="e1")
            >>> e2 = Edge(n2, n3, name="e2")
            >>> graph = {"nodes": [n0, n1, n2, n3], "edges": [e0, e1, e2],}
            >>> InfluenceDiagram.initialize_diagram(graph)
        """
        return cls()

    def get_decision_nodes(self) -> list[DecisionNode]:
        """Return a list of decision nodes

        Returns:
            List[DecisionNode]
        """
        return self._get_nodes_from_type("DecisionNode")

    def get_uncertainty_nodes(self) -> list[UncertaintyNode]:
        """Return a list of uncertainty nodes

        Returns:
            List[UncertaintyNode]
        """
        return self._get_nodes_from_type("UncertaintyNode")

    def get_utility_nodes(self) -> list[UtilityNode]:
        """Return a list of utility nodes

        Returns:
            List[UtilityNode]
        """
        return self._get_nodes_from_type("UtilityNode")

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

    def _to_json_stream(self) -> dict:
        """convert the influence diagram instance into a dictionary
            It uses the method `networkx.node_link_data()`

        Returns:
            Dict: a representation of the diagram
        """
        data = nx.node_link_data(self.nx, source="from", target="to", link="edges")
        data["edges"] = [
            {k: v if not isinstance(v, NodeABC) else v.uuid for k, v in e.items()}
            for e in data["edges"]
        ]
        json_object = json.dumps(data, default=lambda o: o.to_dict(), indent=4)
        return json_object

    @classmethod
    def from_db(cls, response: InfluenceDiagramResponse):
        """Create a diagram from the DataBase Response

        Args:
            response (InfluenceDiagramResponse): The influence diagram as read from
                                                 the database

        Returns:
            ProbabilisticGraphModelABC: the decision diagram

        Example:
            Assume the database returns an influence diagram described in the
            `json_stream`

            >>> influence_diagram_response = \
            ... InfluenceDiagramResponse(vertices=json_stream['vertices'], \
            ... edges=json_stream['edges'])
            >>> InfluenceDiagram.from_db(influence_diagram_response)
        """
        nodes = [NodeABC.from_db(vertex) for vertex in response.nodes]
        arcs = [Edge.from_db(edge, nodes) for edge in response.arcs]
        return cls.from_dict({"nodes": nodes, "edges": arcs})

    def decision_elimination_order(self) -> list[NodeABC]:
        """Decision Elimination Order algorithm

        Returns:
            List[NodeABC] : the decision elimination order graph associated to
                            the influence diagram. Nodes in the list are copies of the
                            nodes of the influence diagram ones.

        TODO: add description of what is the algorithm about
        """
        cid_copy = self.copy()
        decisions = []
        decisions_count = cid_copy.decision_count
        while decisions_count > 0:
            nodes = list(cid_copy.nx.nodes())
            for node in nodes:
                if not cid_copy.has_children(node):
                    if node.is_decision_node:
                        decisions.append(node)
                        decisions_count -= 1
                    cid_copy.nx.remove_node(node)
        return decisions

    def calculate_partial_order(self, mode="view") -> list[NodeABC]:
        """Partial order algorithm


        Args:
            mode (str): ["view"(default)|"copy"]
                returns a view or a copy of the nodes

        Returns
            List[NodeABC]: list of nodes (copies or vioews) sorted in decision order

        TODO: add description of what the algorithm is about
        TODO: handle utility nodes
        """
        if mode not in ["view", "copy"]:
            raise PartialOrderOutputModeError(mode)

        # get all chance nodes
        uncertainty_node = self.get_uncertainty_nodes()
        elimination_order = self.decision_elimination_order()
        # TODO: Add utility nodes
        partial_order = []

        while elimination_order:
            decision = elimination_order.pop()
            parent_decision_nodes = []
            for parent in self.get_parents(decision):
                if not parent.is_decision_node:
                    if parent in uncertainty_node:
                        parent_decision_nodes.append(parent)
                        uncertainty_node.remove(parent)

            if len(parent_decision_nodes) > 0:
                partial_order += parent_decision_nodes
            partial_order.append(decision)

        partial_order += uncertainty_node

        if mode == "copy":
            partial_order = [node.copy() for node in partial_order]

        return partial_order

    def _output_branches_from_node(
        self, node: NodeABC, node_in_partial_order: NodeABC, flip=True
    ) -> list[tuple[Edge, NodeABC]]:
        """Make a list of output branches from a node

            This method actually returns the states of the nodes.

        Args
            node (NodeABC): node to find the output branch from
            node_in_partial_order (NodeABC): associated node in the partial order - to
                                             keep reference too
            flip (bool): if True (default), flip the list of branches so a generated
                         decision tree is in the same order as the entered states.
                         If False, the tree will be flipped horizontally.

        Returns
            List: the list of tuples (Edges, Node in partial order)
                The edges have the input node as start endpoint and name given by the
                state
        """
        if node.is_utility_node:
            tree_stack = [Edge(node, None, name=utility) for utility in node.utility]
        if node.is_decision_node:
            tree_stack = [
                Edge(node, None, name=alternative) for alternative in node.alternatives
            ]
        if node.is_uncertainty_node:
            # This needs to be re-written according to the way we deal with probabilities
            tree_stack = [Edge(node, None, name=outcome) for outcome in node.outcomes]
        if flip:
            tree_stack.reverse()

        return zip(tree_stack, [node_in_partial_order] * len(tree_stack), strict=False)

    def convert_to_decision_tree(self) -> DecisionTree:
        """Convert the influence diagram into a DecisionTree object

        Returns:
            DecisionTree: The symmetric decision tree equivalent to the influence diagram

        TODO: Update ID2DT according to way we deal with probabilities
        """
        partial_order = self.calculate_partial_order()
        root_node = partial_order[0]
        # decision_tree = DecisionTree.initialize_with_root(root_node)
        decision_tree = DecisionTree(root=root_node)
        # tree_stack contains views of the partial order nodes
        # decision_tree contains copy of the nodes (as they appear several times)
        tree_stack = [(root_node, root_node)]

        while tree_stack:
            element = tree_stack.pop()

            if isinstance(element[0], NodeABC):
                tree_stack += self._output_branches_from_node(*element)

            else:  # element is a branch
                endpoint_start_index = partial_order.index(element[1])

                if endpoint_start_index < len(partial_order) - 1:
                    endpoint_end = partial_order[endpoint_start_index + 1].copy()
                    tree_stack.append(
                        (endpoint_end, partial_order[endpoint_start_index + 1])
                    )
                else:
                    # endpoint_end = UtilityNode(
                    #     name=element[0].name, tag=element[0].name.lower()
                    #                           )
                    endpoint_end = UtilityNode(shortname="ut", description="Utility")

                element[0].set_endpoint(endpoint_end)
                decision_tree.add_edge(
                    element[0]
                )  # node is added when the branch is added

        return decision_tree

    @staticmethod
    def _nodes_to_pyagrum(nodes, gum_id):
        # create an uuid for gum as 8 bytes integer and keep relation to uuid
        uuid_dot_to_gum = {}
        uuid_gum_to_dot = {}
        node_uuid = {}

        for node in nodes:
            labelized_variables = [node.shortname, node.description]
            if isinstance(node, UncertaintyNode):
                try:
                    labelized_variables.append(node.outcomes)
                    variable_id = gum_id.addChanceNode(
                        gum.LabelizedVariable(*labelized_variables)
                    )
                except Exception as e:
                    raise ProbabilityFormatError(e)
            elif isinstance(node, DecisionNode):
                # This works even when alternatives are [""] or None
                labelized_variables.append(node.alternatives)
                variable_id = gum_id.addDecisionNode(
                    gum.LabelizedVariable(*labelized_variables)
                )
            elif isinstance(node, UtilityNode):
                # Utility not yet implemented
                labelized_variables.append(1)
                variable_id = gum_id.addUtilityNode(
                    gum.LabelizedVariable(*labelized_variables)
                )

            uuid_dot_to_gum[node.uuid] = variable_id
            uuid_gum_to_dot[variable_id] = node.uuid
            node_uuid[variable_id] = node

        return uuid_dot_to_gum, uuid_gum_to_dot, node_uuid

    @staticmethod
    def _arcs_to_pyagrum(edges, gum_id, uuid_dot_to_gum):
        for arc in edges:
            tail = uuid_dot_to_gum[arc[0].uuid]
            head = uuid_dot_to_gum[arc[1].uuid]
            try:
                gum_id.addArc(tail, head)
            except Exception as e:
                raise ArcFormatError(e)
        return None

    def to_pyagrum(self):
        if not nx.is_directed_acyclic_graph(self.nx):
            raise InfluenceDiagramNotAcyclicError

        gum_id = gum.InfluenceDiagram()
        variable_id = []

        uuid_dot_to_gum, uuid_gum_to_dot, node_uuid = InfluenceDiagram._nodes_to_pyagrum(
            self.nx.nodes, gum_id
        )
        # Add head and tail in gum_id
        InfluenceDiagram._arcs_to_pyagrum(self.nx.edges, gum_id, uuid_dot_to_gum)

        for variable_id in uuid_gum_to_dot:
            if isinstance(node_uuid[variable_id], UncertaintyNode):
                for agrum_prob in node_uuid[variable_id].probabilities.to_pyagrum():
                    gum_id.cpt(variable_id)[agrum_prob[0]] = agrum_prob[1]

        return gum_id
