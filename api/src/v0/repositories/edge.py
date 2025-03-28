from ..database.client import DatabaseClient
from ..models.edge import EdgeResponse
from ..models.meta import EdgeMetaData


class EdgeRepository:
    def __init__(self, client: DatabaseClient):
        self._client = client
        self.builder = client.builder

    def create(
        self, out_vertex_uuid: str, in_vertex_uuid: str, edge_label: str
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
        edge_data = {"inV": in_vertex_uuid, "outV": out_vertex_uuid, "id": ""}
        metadata = EdgeMetaData()
        edge = {**metadata.model_dump(), **edge_data}
        query = self.builder.query.edge.create_edge(
            edge_label, out_vertex_uuid, in_vertex_uuid, edge
        )
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.edge.build_item(results)

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
        query = self.builder.query.edge.list_all_edges_from_project(
            project_uuid, edge_label
        )
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.edge.build_list(results)

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
        query = self.builder.query.edge.list_all_edges_from_sub_project(
            project_uuid, edge_label, vertex_uuid
        )
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.edge.build_list(results)

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
        query = self.builder.query.edge.read_out_edge_from_vertex(
            vertex_uuid, edge_label
        )
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.edge.build_list(results)

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
        query = self.builder.query.edge.read_in_edge_to_vertex(vertex_uuid, edge_label)
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.edge.build_list(results)

    def read(self, edge_uuid: str) -> EdgeResponse:
        """Method to read one edge based on the id

        Args:
            edge_uuid (str): id of the edge

        Returns:
            EdgeResponse: Edge
        """
        query = self.builder.query.edge.read_edge(edge_uuid)
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.edge.build_item(results)

    # # TODO: do we need that? Instead of deleting and creating a new one?
    # def update(self, edge_uuid: str, modified_fields: EdgeUpdate) -> EdgeResponse:
    #     """_summary_

    #     Args:
    #         edge_uuid (str): id of the edge
    #         modified_fields (dict): contains properties of the edge

    #     Returns:
    #         EdgeResponse: Edge
    #     """
    #     query = self.builder.query.edge.update_edge(
    #         edge_uuid, modified_fields.model_dump(exclude_unset=True)
    #     )
    #     with self._client as c:
    #         results = c.execute_query(query)
    #     return self.builder.response.edge.build_item(results)

    def delete(self, edge_uuid: str):
        """Method to delete one edge based on the edge id

        Args:
            edge_uuid (str): id of the edge

        Return:
            None
        """
        query = self.builder.query.edge.delete_edge(edge_uuid)
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.edge.build_none(results)

    def delete_edge_from_vertex(self, vertex_uuid: str) -> None:
        """Deletes edges going in and out of the specified vertex

        Args:
            vertex_uuid (str): id of the vertex

        Return:
            None
        """
        query = self.builder.query.edge.delete_edge_from_vertex(vertex_uuid)
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.edge.build_none(results)
