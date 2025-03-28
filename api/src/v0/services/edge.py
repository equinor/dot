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
        """Create a new edge between two vertices

        Args:
            out_vertex_uuid (str): id of the vertex where the edge goes out
            in_vertex_uuid (str): id of the vertex where the edge goes in
            edge_label (str): label of the edge ("contains" or "influences")

        Return:
            EdgeResponse: Edge (with properties id, outV, inV, uuid, label),
                          where id == uuid

        """
        return self.repository.create(out_vertex_uuid, in_vertex_uuid, edge_label)

    def read_all_edges_from_project(
        self, project_uuid: str, edge_label: str
    ) -> list[EdgeResponse]:
        """Method to return all edges with the specified edge label

        Args:
            project_uuid (str): id of the project vertex
            edge_label (str): label of the edge ("contains" or "influences")

        Returns:
            List[EdgeResponse]: List of Edges
        """
        return self.repository.read_all_edges_from_project(project_uuid, edge_label)

    def read_all_edges_from_sub_project(
        self, project_uuid: str, edge_label: str, vertex_uuid: list[str]
    ) -> list[EdgeResponse]:
        """Method to return all edges with the specified edge label and linking vertices
            with given properties

        Args:
            project_uuid (str): id of the project vertex
            edge_label (str): label of the edge ("contains" or "influences")
            vertex_uuid (list[str]): list of vertices uuid of the sub-project

        Returns:
            List[EdgeResponse]: List of Edges
        """
        return self.repository.read_all_edges_from_sub_project(
            project_uuid, edge_label, vertex_uuid
        )

    def read_out_edge_from_vertex(
        self, vertex_uuid: str, edge_label: str
    ) -> list[EdgeResponse]:
        """Returns edges going out of the specified vertex

        Args:
            vertex_uuid (str): id of the vertex
            edge_label (str): label of the edge
        Return:
            List of edges
        """
        return self.repository.read_out_edge_from_vertex(vertex_uuid, edge_label)

    def read_in_edge_to_vertex(
        self, vertex_uuid: str, edge_label: str
    ) -> list[EdgeResponse]:
        """Returns edges going in to the specified vertex

        Args:
            vertex_uuid (str): id of the vertex
            edge_label (str): label of the edge
        Return:
            List of edges
        """
        return self.repository.read_in_edge_to_vertex(vertex_uuid, edge_label)

    def read(self, edge_uuid: str) -> EdgeResponse:
        """Method to read one edge based on the id

        Args:
            edge_uuid (str): id of the edge

        Returns:
            EdgeResponse: Edge
        """
        return self.repository.read(edge_uuid)

    # def update(self, edge_uuid: str, edge_data: EdgeUpdate) -> EdgeResponse:
    #     return self.repository.update(edge_uuid, edge_data)

    def delete(self, edge_uuid: str) -> None:
        """Deletes edges going in and out of the specified vertex

        Args:
            vertex_uuid (str): id of the vertex

        Return:
            None
        """
        return self.repository.delete(edge_uuid)
