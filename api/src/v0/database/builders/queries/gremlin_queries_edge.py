from .query_builder import GremlinStringQueryBuilder


class GremlinStringQueryBuilderEdge(GremlinStringQueryBuilder):
    """
    Specialized GremlinStringQueryBuilder for constructing Gremlin queries related
        to edges.

    Inherits common query building methods from GremlinStringQueryBuilder and adds
    methods for
    creating, reading, updating, and deleting edges.
    """

    def create_edge(
        self,
        edge_label: str,
        out_vertex_uuid: str,
        in_vertex_uuid: str,
        edge_dict: dict[str, str],
    ) -> str:
        """
        Generates a Gremlin query string to create a new edge between specified vertices
            with the given label and properties.

        Args:
            edge_label (str): Label of the edge to create.
            out_vertex_uuid (str): UUID of the outgoing vertex.
            in_vertex_uuid (str): UUID of the incoming vertex.
            edge_dict (dict[str, str]): Dictionary of property key-value pairs for
                                        the edge.

        Returns:
            str: Gremlin query string for creating the edge.
        """

        query = f"{self.graph_name}.V('{out_vertex_uuid}').addE('{edge_label}')"
        query += f".to(__.V('{in_vertex_uuid}'))"
        query += self.property_query("id", edge_dict["uuid"])
        query += self.property_query("uuid", edge_dict["uuid"])

        return query

    def read_edge(self, edge_id: str) -> str:
        """
        Generates a Gremlin query string to retrieve an edge by its ID.

        Args:
            edge_id (str): ID of the edge to read.

        Returns:
            str: Gremlin query string for reading the edge.
        """

        return f"{self.graph_name}.E('{edge_id}')"

    def list_all_edges(
        self, edge_label: str, filter_dict: dict[str, str] | None = None
    ) -> str:
        """
        Generates a Gremlin query string to list all edges with a specific label,
        optionally filtering by additional properties.

        Args:
            edge_label (str): Label of the edges to list.
            filter_dict (dict[str, str] | None): Optional dictionary of property
                                                 key-value pairs to filter the edges.

        Returns:
            str: Gremlin query string for listing the edges.
        """

        query = f"{self.graph_name}.E()" + self.filter_label_query(edge_label)

        if filter_dict is not None:
            query += self.filter_query(filter_dict)

        query += self.transform_query

        return query

    def list_all_edges_from_project(self, project_uuid: str, edge_label: str) -> str:
        """
        Generates a Gremlin query string to list all edges of a specific label
            originating from a given project vertex.

        Args:
            project_uuid (str): UUID of the project vertex.
            edge_label (str): Label of the edges to list.

        Returns:
            str: Gremlin query string for listing the edges.
        """
        query = f"{self.graph_name}.V('{project_uuid}').outE('contains')"

        if edge_label == "influences":
            query += ".inV().outE('influences')"
        elif edge_label == "merged_into":
            query += ".inV().inE('merged_into')"
        elif edge_label == "has_value_metric":
            query += ".inV().outE('has_value_metric')"

        return query

    def list_all_edges_from_sub_project(
        self, project_uuid: str, edge_label: str, vertex_uuid: list[str]
    ) -> str:
        """
        Generates a Gremlin query string to list all edges with the specified edge label
            and linking vertices with given properties

        Args:
            project_uuid (str): id of the project vertex
            edge_label (str): label of the edge ("contains" or "influences")
            vertex_uuid (list[str]): list of vertices uuid of the sub-project

        Returns:
            str: Gremlin query string for listing the edges.
        """
        query = f"g.V('{project_uuid}').outE('contains').inV().outE('{edge_label}')"
        query += ".where("
        query += "and("
        query += f"__.inV().has('uuid', within({vertex_uuid})),"
        query += f"__.outV().has('uuid', within({vertex_uuid}))"
        query += ")"
        query += ")"
        query += ""

        return query

    def read_out_edge_from_vertex(self, vertex_uuid: str, edge_label: str):
        """
        Generates a Gremlin query string to read all outgoing edges from a vertex given
            an edge label.

        Args:
            vertex_uuid (str): ID of the vertex.
            edge_label (str): label of the edges to read

        Returns:
            str: Gremlin query string for reading the edges.
        """
        query = f"{self.graph_name}.V('{vertex_uuid}').outE()"
        query += self.filter_label_query(edge_label)
        return query

    def read_in_edge_to_vertex(self, vertex_uuid: str, edge_label: str):
        """
        Generates a Gremlin query string to read all incoming edges to a vertex given an
            edge label.

        Args:
            vertex_uuid (str): ID of the vertex.
            edge_label (str): label of the edges to read

        Returns:
            str: Gremlin query string for reading the edges.
        """
        query = f"{self.graph_name}.V('{vertex_uuid}').inE()"
        query += self.filter_label_query(edge_label)
        return query

    def update_edge(self, edge_id: str, edge_prop: dict[str, str]) -> str:
        """
        Generates a Gremlin query string to update the properties of an existing edge.

        Args:
            edge_id (str): ID of the edge to update.
            edge_prop (dict[str, str]): Dictionary of property key-value pairs to update.

        Returns:
            str: Gremlin query string for updating the edge.
        """

        query = f"{self.graph_name}.E('{edge_id}')"
        query += self.property_dict_query(edge_prop)
        return f"[{query}]"

    def delete_edge(self, edge_id: str) -> str:
        """
        Generates a Gremlin query string to delete an edge by its ID.

        Args:
            edge_id (str): ID of the edge to delete.

        Returns:
            str: Gremlin query string for deleting the edge.
        """
        return f"{self.graph_name}.E('{edge_id}').drop()"

    def delete_edge_from_vertex(self, vertex_id: str) -> str:
        """
        Generates a Gremlin query string to delete all edges connected to a given vertex.

        Args:
            vertex_id (str): ID of the vertex to remove edges from.

        Returns:
            str: Gremlin query string for deleting the edges.
        """

        return f"{self.graph_name}.V('{vertex_id}').bothE().drop()"
