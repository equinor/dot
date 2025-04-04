# from src.v0.models.structure import InfluenceDiagramResponse
# from src.v0.models.structure import DecisionTreeNodeResponse
# from src.v0.models.edge import EdgeResponse
# from src.v0.models.issue import IssueResponse

from src.v0.services.classes.arc import Arc
from src.v0.services.classes.node import NodeABC
# from src.v0.services.structure_utils.decision_diagrams.influence_diagram import InfluenceDiagram
# from src.v0.services.structure_utils.decision_diagrams.decision_tree import DecisionTree

from .node import InfluenceDiagramNodeConversion

from ..errors import ArcTypeError




class ArcConversion:
    def from_json(self, edge: dict, issues: list[dict]) -> Arc:
        if not ("outV" in edge.keys() and "inV" in edge.keys()):
            raise ArcTypeError(list(edge.keys()))

        tails = [issue for issue in issues if issue["uuid"] == edge["outV"]]
        heads = [issue for issue in issues if issue["uuid"] == edge["inV"]]

        if not (len(tails) == 1 and len(heads) == 1):
            raise ArcTypeError((tails, heads))

        return Arc(
            tail=InfluenceDiagramNodeConversion().from_json(tails[0]),
            head=InfluenceDiagramNodeConversion().from_json(heads[0])
            )
    
    def to_json(self, arc: Arc, nodes: list[NodeABC]) -> dict:
        outV = [node.uuid for node in nodes if node == arc.tail][0]
        inV = [node.uuid for node in nodes if node == arc.head][0]
        return {
            "outV": outV,
            "inV": inV,
            "uuid": arc.uuid,
            "id": arc.uuid,
            "label": "influences"
        }
