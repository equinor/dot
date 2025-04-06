from src.v0.services.classes.influence_diagram import InfluenceDiagram

from ..errors import InfluenceDiagramTypeError
from .arc import ArcConversion
from .node import InfluenceDiagramNodeConversion


class InfluenceDiagramConversion:
    def from_json(self, influence_diagram: dict) -> InfluenceDiagram:
        if (nodes := influence_diagram.get("nodes", None)) is None:
            raise InfluenceDiagramTypeError(None)

        diagram = InfluenceDiagram()
        try:
            for node_of_id in nodes:
                diagram.add_node(InfluenceDiagramNodeConversion().from_json(node_of_id))
            diagram.add_arcs(
                [
                    ArcConversion().from_json(arc, nodes)
                    for arc in influence_diagram["arcs"]
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
            "arcs": [
                ArcConversion().to_json(item, influence_diagram.nodes)
                for item in influence_diagram.arcs
            ],
        }


# class DecisionTreeConversion:
#     def from_json(self, decision_tree: dict) -> DecisionTree:
#         pass

#     def to_json(self, decision_tree: DecisionTree) -> Dict:
#         pass

# def from_influence_diagram_response(
#         self,
#         decision_tree: DecisionTreeResponse
#         ) -> DecisionTree:
#     as_dict = decision_tree.model_dump(mode='json')
#     return self.from_json(as_dict)

# def to_influence_diagram_response(
#         self,
#         decision_tree: DecisionTree
#         ) -> DecisionTreeResponse:
#     return DecisionTreeResponse.model_validate(self.to_json(decision_tree))
