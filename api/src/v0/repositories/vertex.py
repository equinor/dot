from ..database.client import DatabaseClient
from ..models.filter import Filter
from ..models.meta import VertexMetaData
from ..models.vertex import VertexCreate, VertexResponse, VertexUpdate


class VertexRepository:
    def __init__(self, client: DatabaseClient):
        self._client = client
        self.builder = client.builder

    def create(self, vertex_label: str, vertex: VertexCreate) -> VertexResponse:
        """Creates a new vertex based on vertex data

        Args:
            vertex_label (str): given vertex label for gremlin DB, e.g. "issue",
                                "project", "opportunity", "objective"
            vertex (VertexCreate): data for properties in vertex
                provides generated uuid
                provides uuid will also be set as the id in the DB

        Return:
            VertexResponse: dict of the created vertex

        """
        metadata = VertexMetaData()
        vertex_data = {**metadata.model_dump(), **vertex.model_dump()}
        query = self.builder.query.vertex.create_vertex(vertex_label, vertex_data)
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.vertex.build_item(results)

    def read(self, vertex_uuid: str) -> VertexResponse:
        """Reads a vertex based on the vertex id in the DB

        Args:
            vertex_uuid (str): uuid of the vertex.

                uuid property [g.V().property("uuid",...)] and vertex id [g.V(id)] are
                the same based on the implementation in the create method
                This is an active choice of us, otherwise, the id will be automatically
                generated in the DB

        Return:
            VertexResponse: dict with all data of the vertex (VertexResponse)
        """
        query = self.builder.query.vertex.read_vertex(vertex_uuid)
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.vertex.build_item(results)

    def read_out_vertex(
        self,
        vertex_uuid: str,
        edge_label: str,
        original_vertex_label: str = None,
        filter_model: Filter = None,
    ) -> list[VertexResponse]:
        """Read vertices based on outgoing edge labels.

        Args:
            vertex_uuid (str): id of the vertex
            edge_label (str): edge label, e.g. "contains" or "influences"
            original_vertex_label (str, optional): label of the vertices we are
                                                   interested in (e.g. only issues or
                                                   also opportunities and objectives).
                                                   Defaults to None.
            filter_model (Filter, optional): BaseModel containing properties to use as
                                             a filter, for example the type or tag of
                                             vertices. Defaults to None.

        Returns:
            List[VertexResponse]:
                List of all vertices connected to the vertex with the vertex id
                vertex_uuid through an edge with the label edge_label
                When original_vertex_label is given the vertices will be filtered
                based on the label of the vertex, e.g. it will return either "issue",
                "opportunity" or "objective" vertices otherwise, all vertices are
                returned
                When filter_model is given, the vertices will be filtered based on the
                content of the filter model. Currently this can be "tag", "type",...
                and other properties of the vertices defined in the database
                If filter_model is None, no filter will be applied and all vertices will
                be returned.
        """
        filter_dict = None if filter_model is None else filter_model.model_dump()
        query = self.builder.query.vertex.read_out_vertex(
            vertex_uuid, edge_label, original_vertex_label, filter_dict
        )
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.vertex.build_list(results)

    def read_in_vertex(
        self,
        vertex_uuid: str,
        edge_label: str,
        original_vertex_label: str = None,
        filter_model: Filter = None,
    ) -> list[VertexResponse]:
        """Read vertices based on incoming edge labels.

        Args:
            vertex_uuid (str): id of the vertex
            edge_label (str): edge label, e.g. "contains" or "influences"
            original_vertex_label (str, optional): label of the vertices we are
                                                   interested in (e.g. only issues or
                                                   also opportunities and objectives).
                                                   Defaults to None.
            filter_model (Filter, optional): BaseModel containing properties to use
                                             as a filter, for example the type or tag
                                             of vertices. Defaults to None.

        Returns:
            List[VertexResponse]: List of all vertices connected to the vertex with
                                  the vertex id vertex_uuid through an incoming edge
                                  with the label edge_label

                When original_vertex_label is given, the vertices will be filtered
                based on the label of the vertex, e.g. it will return either "issue",
                "opportunity" or "objective" vertices. Otherwise, all vertices are
                returned.
                When filter_model is given, the vertices will be filtered based on
                the content of the filter model. Currently, this can be "tag", "type",
                and other properties of the vertices defined in the database.
                If filter_model is None, no filter will be applied and all vertices will
                be returned.
        """
        filter_dict = None if filter_model is None else filter_model.model_dump()
        query = self.builder.query.vertex.read_in_vertex(
            vertex_uuid, edge_label, original_vertex_label, filter_dict
        )
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.vertex.build_list(results)

    # Not sure if this is needed
    # def all(self, vertex_label: str, filter_dict: dict = None) -> List[VertexResponse]:
    def all(self, vertex_label: str) -> list[VertexResponse]:
        """Read all vertices given a label

        Args:
            vertex_label (str): label of vertices to read (e.g. opportunity)

        Returns:
            list[VertexResponse]: list of vertices with the given label
        """
        query = self.builder.query.vertex.list_all_vertices(vertex_label)
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.vertex.build_list(results)

    def update(self, vertex_uuid: str, modified_fields: VertexUpdate) -> VertexResponse:
        """Updated the specified vertex with the new vertex properties

        Args:
            vertex_uuid (str): id of the to be updated vertex
            modified_fields (VertexUpdate): properties of vertices which will
                                            be updated

        Return:
            VertexResponse: vertex dict with updated properties
        """
        query = self.builder.query.vertex.update_vertex(
            vertex_uuid, modified_fields.model_dump(exclude_unset=True)
        )
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.vertex.build_item(results)

    def delete(self, vertex_uuid: str) -> None:
        """method to delete a vertex based on the vertex id

        Args:
            vertex_uuid (str): id of the vertex which will be deleted

        Return:
            None
        """
        query = self.builder.query.vertex.delete_vertex(vertex_uuid)
        with self._client as c:
            results = c.execute_query(query)
        return self.builder.response.vertex.build_none(results)
