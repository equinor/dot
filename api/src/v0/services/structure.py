import json

from src.v0.services.structure_utils.decision_diagrams.influence_diagram import (
    InfluenceDiagram,
)

from ..models.filter import Filter
from ..models.issue import IssueResponse
from ..models.structure import (
    DecisionTreeResponse,
    InfluenceDiagramResponse,
)
from ..repositories.edge import EdgeRepository
from ..repositories.vertex import VertexRepository


class StructureService:
    def __init__(self, repository: VertexRepository):
        self.repository = repository

    def read_influence_diagram(self, project_uuid: str) -> InfluenceDiagramResponse:
        """Method to read the necessary data to create the influence diagram structure

        Args:
            project_uuid (str): id of the project vertex

        Returns
            InfluenceDiagramResponse: Dict of vertices and edges
        """
        edge_repository = EdgeRepository(self.repository._client)

        # read nodes (uncertainty, decision, valuemetric category)
        vertices = []

        # In boundary
        for vertex_category in ["Uncertainty", "Decision", "Value Metric"]:
            for boundary in ["in", "on"]:
                filter_model = Filter(category=vertex_category, boundary=boundary)
                if vertex_category == "Uncertainty":
                    filter_model.keyUncertainty = "true"
                elif vertex_category == "Decision":
                    filter_model.decisionType = "Focus"
                vertex = self.repository.read_out_vertex(
                    vertex_uuid=project_uuid,
                    original_vertex_label="issue",
                    edge_label="contains",
                    filter_model=filter_model,
                )
                vertices.extend(vertex)

        # create list of Issue objects from vertices
        issues_list = [
            IssueResponse.model_validate(v.model_dump()) for v in vertices if v
        ]
        edges = edge_repository.read_all_edges_from_sub_project(
            project_uuid=project_uuid,
            edge_label="influences",
            vertex_uuid=[issue.uuid for issue in issues_list],
        )

        influence_diagram = InfluenceDiagramResponse(vertices=issues_list, edges=edges)
        return influence_diagram

    def create_decision_tree(self, project_uuid: str) -> DecisionTreeResponse:
        """Method to read the necessary data to create the decision tree structure

        Args:
            project_uuid (str): id of the project vertex

        Returns
            DecisionTreeResponse: Dict of vertices
        """
        influence_diagram = self.read_influence_diagram(project_uuid=project_uuid)
        local_id = InfluenceDiagram.from_db(influence_diagram)
        # local_id.to_json("id.json")
        local_dt = local_id.convert_to_decision_tree()
        # dt_json = json.loads(local_dt.to_json("dt.json"))
        dt_json = json.loads(local_dt.to_json())
        decision_tree = DecisionTreeResponse.model_validate(dt_json)
        return decision_tree
