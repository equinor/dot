from ..database.client import DatabaseClient
from ..models.filter import Filter
from ..models.issue import IssueCreate, IssueResponse, IssueUpdate
from ..repositories.edge import EdgeRepository
from ..repositories.vertex import VertexRepository


class IssueRepository:
    def __init__(self, client: DatabaseClient):
        self._client = client
        self.builder = client.builder

    def read(self, issue_uuid: str) -> IssueResponse:
        """Method to read one issue based on the id

        Args:
            issue_uuid (str): id of the vertex with the label "issue"

        Returns:
            IssueResponse: Issue with all properties
        """
        vertex = VertexRepository(self._client).read(issue_uuid)
        return IssueResponse.convert_api_payload_to_response(vertex)

    def read_issues_all(
        self,
        project_uuid: str,
        vertex_label: str,
        edge_label: str,
        filter_model: Filter,
    ) -> list[IssueResponse]:
        """Read all issues connected to one project with filter possibilities

        Args:
            project_uuid (str): id of the project vertex
            vertex_label (str): label of the vertices of interest
            edge_label (str): edge_label to clarify the connection between the project
                              node and issue node, should always be "contains" in this
                              method (default "contains")
            filter_model (Filter(BaseModel)): contains a dict with different properties
                                              for filtering, like category, tag,
                                              shortname

        Returns:
            List[IssueResponse]: List of Issues which satisfy the condition to be
                                 connected to the Project vertex with a "contains" edge
                                 and have the label "issue" and satisfy the filters
                                 when given in filter_model
        """
        vertex_list = VertexRepository(self._client).read_out_vertex(
            vertex_uuid=project_uuid,
            edge_label=edge_label,
            original_vertex_label=vertex_label,
            filter_model=filter_model,
        )
        return IssueResponse.convert_list_api_payloads_to_responses(vertex_list)

    def create(self, project_uuid: str, issue_data: IssueCreate) -> IssueResponse:
        """Method to create a new issue connected to a project vertex

            Creates vertex with the label "issue" and the properties of issue_data
            Creates an edge between the project vertex specified by project_uuid and
            the newly create issue vertex

        Args:
            project_uuid (str): id of the project vertex the new issue will be
                                connected to
            issue_data (IssueCreate): contains all properties for the issue

        Returns:
            IssueResponse: Created Issue with the issue_data as IssueCreate
        """
        vertex = VertexRepository(self._client).create("issue", issue_data)
        EdgeRepository(self._client).create(
            out_vertex_uuid=project_uuid,
            in_vertex_uuid=vertex.uuid,
            edge_label="contains",
        )
        return IssueResponse.convert_api_payload_to_response(vertex)

    def update(self, issue_uuid: str, modified_fields: IssueUpdate) -> IssueResponse:
        """Updates the specified issue based on the id with the new issue_data

        Args:
            issue_uuid (str): id of the issue vertex
            modified_fields (IssueUpdate): contains properties of the issue

        Returns:
            IssueResponse: Issue with the issue_data as IssueCreate
        """
        if ("boundary" in modified_fields.model_dump(exclude_unset=True)) and (
            modified_fields.boundary not in ["in", "on"]
        ):
            modified_fields.decisionType = None
            modified_fields.keyUncertainty = None

        vertex = VertexRepository(self._client).update(issue_uuid, modified_fields)
        # if boundary is not 'in' or 'on' anymore, remove decision type and key
        # uncertainty, and remove "influences" edges from parents or children
        if vertex.boundary not in ["in", "on"]:
            out_edges = EdgeRepository(self._client).read_out_edge_from_vertex(
                issue_uuid, edge_label="influences"
            )
            in_edges = EdgeRepository(self._client).read_in_edge_to_vertex(
                issue_uuid, edge_label="influences"
            )
            for edge in out_edges:
                EdgeRepository(self._client).delete(edge.uuid)
            for edge in in_edges:
                EdgeRepository(self._client).delete(edge.uuid)
        return IssueResponse.convert_api_payload_to_response(vertex)

    def delete(self, issue_uuid: str) -> None:
        """Deletes the issue vertex based on the id and also all in and outgoing edges
            from this vertex

        Args:
            issue_uuid (str): id of the issue vertex

        Returns:
            None
        """
        EdgeRepository(self._client).delete_edge_from_vertex(issue_uuid)
        VertexRepository(self._client).delete(issue_uuid)
        return None
