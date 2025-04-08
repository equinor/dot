import json

import networkx as nx

from src.v0.services.classes.decision_tree import DecisionTree
from src.v0.services.classes.influence_diagram import InfluenceDiagram
from src.v0.services.errors import InfluenceDiagramTypeError, RootNodeNotFound
from src.v0.services.format_conversions.node import DecisionTreeNodeConversion

from .arc import ArcConversion
from .node import InfluenceDiagramNodeConversion


class InfluenceDiagramConversion:
    def from_json(self, influence_diagram: dict) -> InfluenceDiagram:
        if (nodes := influence_diagram.get("vertices", None)) is None:
            raise InfluenceDiagramTypeError(None)

        diagram = InfluenceDiagram()
        try:
            for node_of_id in nodes:
                diagram.add_node(InfluenceDiagramNodeConversion().from_json(node_of_id))
            diagram.add_arcs(
                [
                    ArcConversion().from_json(arc, nodes)
                    for arc in influence_diagram["edges"]
                ]
            )
            return diagram
        except Exception:
            raise InfluenceDiagramTypeError(None)

    def to_json(self, influence_diagram: InfluenceDiagram) -> dict:
        return {
            "nodes": [
                InfluenceDiagramNodeConversion().to_json(item)
                for item in influence_diagram.nodes
            ],
            "vertices": [
                ArcConversion().to_json(item, influence_diagram.nodes)
                for item in influence_diagram.arcs
            ],
        }


class DecisionTreeConversion:
    def from_json(self, decision_tree: dict) -> DecisionTree:
        raise NotImplementedError

    def to_json(self, decision_tree: DecisionTree) -> dict:
        def propagate_branch_name(decision_tree, node, names):
            predecessor = decision_tree.parent(node)
            if not predecessor:
                return ""
            n = names[(predecessor, node)]
            return n if isinstance(n, str) else "-".join(n)

        if decision_tree.root is None:
            raise RootNodeNotFound(None)

        edges_name = nx.get_edge_attributes(decision_tree.graph, "label")
        tg = nx.readwrite.json_graph.tree_data(decision_tree.graph, decision_tree.root)
        json_object = json.dumps(
            tg,
            default=lambda node: {
                **DecisionTreeNodeConversion().to_json(
                    DecisionTreeNodeConversion().from_json(
                        InfluenceDiagramNodeConversion().to_json(node)
                        | {
                            "branch_name": propagate_branch_name(
                                decision_tree, node, edges_name
                            )
                        }
                    )
                )
            },
            indent=2,
        )
        return json.loads(json_object)
