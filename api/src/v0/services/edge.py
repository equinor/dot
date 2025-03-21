from ..models.edge import EdgeResponse
from ..repositories.edge import EdgeRepository


class EdgeService:
    def __init__(self, repository: EdgeRepository):
        self.repository = repository

    def create(
        self,
        out_vertex_uuid: str,
        in_vertex_uuid: str,
        edge_label: str,
    ) -> EdgeResponse:
        return self.repository.create(out_vertex_uuid, in_vertex_uuid, edge_label)

    def read_all_edges_from_project(
        self, project_uuid: str, edge_label: str
    ) -> list[EdgeResponse]:
        return self.repository.read_all_edges_from_project(project_uuid, edge_label)

    def read_all_edges_from_sub_project(
        self, project_uuid: str, edge_label: str, vertex_uuid: list[str]
    ) -> list[EdgeResponse]:
        return self.repository.read_all_edges_from_sub_project(
            project_uuid, edge_label, vertex_uuid
        )

    def read_out_edge_from_vertex(
        self, vertex_uuid: str, edge_label: str
    ) -> list[EdgeResponse]:
        return self.repository.read_out_edge_from_vertex(vertex_uuid, edge_label)

    def read_in_edge_to_vertex(
        self, vertex_uuid: str, edge_label: str
    ) -> list[EdgeResponse]:
        return self.repository.read_in_edge_to_vertex(vertex_uuid, edge_label)

    def read(self, edge_uuid: str) -> EdgeResponse:
        return self.repository.read(edge_uuid)

    # def update(self, edge_uuid: str, edge_data: EdgeUpdate) -> EdgeResponse:
    #     return self.repository.update(edge_uuid, edge_data)

    def delete(self, edge_uuid: str) -> None:
        return self.repository.delete(edge_uuid)
