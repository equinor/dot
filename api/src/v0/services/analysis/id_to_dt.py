"""
Conversion of influence diagram to decision tree.
The decision tree format is used for display in the frontend.
"""

from src.v0.services.classes.arc import Arc
from src.v0.services.classes.decision_tree import DecisionTree
from src.v0.services.classes.influence_diagram import InfluenceDiagram
from src.v0.services.classes.node import NodeABC, UtilityNode
from src.v0.services.errors import PartialOrderOutputModeError


class InfluenceDiagramToDecisionTree:
    def decision_elimination_order(
        self, influence_diagram: InfluenceDiagram
    ) -> list[NodeABC]:
        """Decision Elimination Order algorithm

        Args:
            influence_diagram (InfluenceDiagram): the influence diagram object
            to convert

        Returns:
            list[NodeABC] : the decision elimination order graph associated to
                            the influence diagram. Nodes in the list are copies of the
                            nodes of the influence diagram ones.

        TODO: add description of what is the algorithm about
        """
        cid_copy = influence_diagram.copy()
        decisions = []
        decisions_count = cid_copy.decision_count
        while decisions_count > 0:
            nodes = list(cid_copy.graph.nodes())
            for node in nodes:
                if not cid_copy.has_children(node):
                    if node.is_decision_node:
                        decisions.append(node)
                        decisions_count -= 1
                    cid_copy.graph.remove_node(node)
        return decisions

    def calculate_partial_order(
        self, influence_diagram: InfluenceDiagram, *, mode="view"
    ) -> list[NodeABC]:
        """Partial order algorithm


        Args:
            influence_diagram (InfluenceDiagram): the influence diagram object
            to convert
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
        uncertainty_node = influence_diagram.get_uncertainty_nodes()
        elimination_order = self.decision_elimination_order(influence_diagram)
        # TODO: Add utility nodes
        partial_order = []

        while elimination_order:
            decision = elimination_order.pop()
            parent_decision_nodes = []
            for parent in influence_diagram.get_parents(decision):
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
    ) -> list[tuple[Arc, NodeABC]]:
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
            List: the list of tuples (Arc, Node in partial order)
                The edges have the input node as start endpoint and name given by the
                state
        """
        if node.is_utility_node:
            tree_stack = [
                Arc(tail=node, head=None, label=utility) for utility in node.utility
            ]
        if node.is_decision_node:
            tree_stack = [
                Arc(tail=node, head=None, label=alternative)
                for alternative in node.alternatives
            ]
        if node.is_uncertainty_node:
            # This needs to be re-written according to the way we deal with probabilities
            tree_stack = [
                Arc(tail=node, head=None, label=outcome) for outcome in node.outcomes
            ]
        if flip:
            tree_stack.reverse()

        return zip(tree_stack, [node_in_partial_order] * len(tree_stack), strict=False)

    def conversion(self, influence_diagram: InfluenceDiagram) -> DecisionTree:
        """Convert the influence diagram into a DecisionTree object

        Returns:
            DecisionTree: The symmetric decision tree equivalent to the influence diagram

        TODO: Update ID2DT according to way we deal with probabilities
        """
        partial_order = self.calculate_partial_order(influence_diagram)
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
                tail_index = partial_order.index(element[1])

                if tail_index < len(partial_order) - 1:
                    head = partial_order[tail_index + 1].copy()
                    tree_stack.append((head, partial_order[tail_index + 1]))
                else:
                    # head = UtilityNode(
                    #     name=element[0].name, tag=element[0].name.lower()
                    #                           )
                    head = UtilityNode(shortname="ut", description="Utility")

                element[0].head = head
                decision_tree.add_arc(
                    element[0]
                )  # node is added when the branch is added

        return decision_tree
