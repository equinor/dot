from copy import deepcopy

from .query_builder import GremlinStringQueryBuilder


class GremlinStringQueryBuilderVertex(GremlinStringQueryBuilder):
    """
    Specialized GremlinStringQueryBuilder for constructing Gremlin queries related
        to vertices.

    Inherits common query building methods from GremlinStringQueryBuilder and adds
    methods for
    creating, reading, updating, and deleting vertices.
    """

    def create_vertex(self, vertex_label: str, vertex_dict: dict[str, str]) -> str:
        """
        Generates a Gremlin query string to create a new vertex with the specified
        label and properties.

        Args:
            vertex_label (str): Label of the vertex to create.
            vertex_dict (dict[str, str]): Dictionary of property key-value pairs for
                                          the vertex.

        Returns:
            str: Gremlin query string for creating the vertex.
        """

        query = f"{self.graph_name}.addV('{vertex_label}')"
        query += self.property_query(
            "id", vertex_dict["uuid"]
        )  # TODO: still copying `uuid` to `id`, check other calls
        query += self.property_dict_query(vertex_dict)
        query += self.transform_query

        return query

    def read_vertex(self, vertex_uuid: str) -> str:
        """
        Generates a Gremlin query string to retrieve a vertex by its UUID.

        Args:
            vertex_uuid (str): UUID of the vertex to read.

        Returns:
            str: Gremlin query string for reading the vertex.
        """

        query = f"{self.graph_name}.V('{vertex_uuid}')"
        query += self.transform_query

        return query

    def read_out_vertex(
        self,
        vertex_uuid: str,
        edge_label: str,
        original_vertex_label: str | None = None,
        filter_dict: dict[str, str] | None = None,
    ) -> str:
        """
        Generates a Gremlin query string to traverse to outgoing vertices along a
        specified edge label,
        optionally filtering by original vertex label and additional properties.

        Args:
            vertex_uuid (str): UUID of the starting vertex.
            edge_label (str): Label of the edges to traverse.
            original_vertex_label (str | None): Optional label to filter the traversed
                                                vertices.
            filter_dict (dict[str, str] | None): Optional dictionary of property
                                                 key-value pairs to filter the traversed
                                                 vertices.

        Returns:
            str: Gremlin query string for the traversal.
        """

        query = f"{self.graph_name}.V('{vertex_uuid}')"
        query += f".out('{edge_label}')"

        if original_vertex_label is not None:
            query += self.filter_label_query(original_vertex_label)

        if filter_dict is not None:
            query += self.filter_query(filter_dict)

        query += self.transform_query

        return query

    def read_in_vertex(
        self,
        vertex_uuid: str,
        edge_label: str,
        original_vertex_label: str | None = None,
        filter_dict: dict[str, str] | None = None,
    ) -> str:
        """
        Generates a Gremlin query string to traverse to ingoing vertices along a
        specified edge label,
        optionally filtering by original vertex label and additional properties.

        Args:
            vertex_uuid (str): UUID of the receiving vertex.
            edge_label (str): Label of the edges to traverse.
            original_vertex_label (str | None): Optional label to filter the traversed
                                                vertices.
            filter_dict (dict[str, str] | None): Optional dictionary of property
                                                 key-value pairs to filter the
                                                 traversed vertices.

        Returns:
            str: Gremlin query string for the traversal.
        """
        query = f"{self.graph_name}.V('{vertex_uuid}')"
        query += f".in('{edge_label}')"

        if original_vertex_label is not None:
            query += self.filter_label_query(original_vertex_label)

        if filter_dict is not None:
            query += self.filter_query(filter_dict)

        query += self.transform_query

        return query

    def list_all_vertices(self, vertex_label: str) -> str:
        """
        Generates a Gremlin query string to list all vertices with a specific label,
        optionally filtering by additional properties.

        Args:
            vertex_label (str): Label of the vertices to list.

        Returns:
            str: Gremlin query string for listing the vertices.
        """
        # the filter is removed as the associated routers either do not implement the
        # method or calls it without the filter.
        query = f"{self.graph_name}.V()" + self.filter_label_query(vertex_label)
        query += self.transform_query

        return query

    def update_vertex(self, vertex_uuid: str, vertex_prop: dict[str, str]) -> str:
        """
        Generates a Gremlin query string to update the properties of an existing vertex.

        Args:
            vertex_uuid (str): UUID of the vertex to update.
            vertex_prop (dict[str, str]): Dictionary of property key-value pairs to
                                          update.

        Returns:
            str: Gremlin query string for updating the vertex.
        """
        properties = deepcopy(vertex_prop)
        properties.pop("id", None)
        properties.pop("label", None)
        query = f"{self.graph_name}.V('{vertex_uuid}')"
        query += self.property_dict_query(properties)
        query += self.transform_query

        return query

    def delete_vertex(self, vertex_uuid: str) -> str:
        """
        Generates a Gremlin query string to delete a vertex by its UUID.

        Args:
            vertex_uuid (str): UUID of the vertex to delete.

        Returns:
            str: Gremlin query string for deleting the vertex.
        """

        return f"{self.graph_name}.V('{vertex_uuid}').drop()"
