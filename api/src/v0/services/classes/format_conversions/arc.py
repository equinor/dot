from src.v0.services.classes.arc import Arc
from src.v0.services.classes.node import NodeABC

from ..errors import ArcTypeError
from .node import InfluenceDiagramNodeConversion


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
            head=InfluenceDiagramNodeConversion().from_json(heads[0]),
        )

    def to_json(self, arc: Arc, nodes: list[NodeABC]) -> dict:
        outV = [node.uuid for node in nodes if node == arc.tail][0]
        inV = [node.uuid for node in nodes if node == arc.head][0]
        return {
            "outV": outV,
            "inV": inV,
            "uuid": arc.uuid,
            "id": arc.uuid,
            "label": "influences",
        }
