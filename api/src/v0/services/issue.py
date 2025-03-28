from ..models.filter import Filter
from ..models.issue import IssueCreate, IssueResponse, IssueUpdate
from ..repositories.edge import EdgeRepository
from ..repositories.issue import IssueRepository
from .issue_utils.issue_merge import issue_merge


class IssueService:
    def __init__(self, repository: IssueRepository):
        self.repository = repository

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
        return self.repository.create(
            project_uuid=project_uuid,
            issue_data=issue_data,
        )

    def read_issues_all(
        self,
        project_uuid: str,
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
        return self.repository.read_issues_all(
            project_uuid=project_uuid,
            vertex_label="issue",
            edge_label="contains",
            filter_model=filter_model,
        )

    def read(self, issue_uuid: str) -> IssueResponse:
        """Method to read one issue based on the id

        Args:
            issue_uuid (str): id of the vertex with the label "issue"

        Returns:
            IssueResponse: Issue with all properties
        """
        return self.repository.read(issue_uuid)

    def update(self, issue_uuid: str, modified_fields: IssueUpdate) -> IssueResponse:
        """Updates the specified issue based on the id with the new issue_data

        Args:
            issue_uuid (str): id of the issue vertex
            modified_fields (IssueUpdate): contains properties of the issue

        Returns:
            IssueResponse: Issue with the issue_data as IssueCreate
        """
        return self.repository.update(issue_uuid, modified_fields)

    def delete(self, issue_uuid: str) -> None:
        """Deletes the issue vertex based on the id and also all in and outgoing edges
            from this vertex

        Args:
            issue_uuid (str): id of the issue vertex

        Returns:
            None
        """
        return self.repository.delete(issue_uuid)

    def merge(
        self,
        project_uuid: str,
        source_issue: IssueResponse,
        destination_issue: IssueResponse,
    ) -> IssueResponse:
        """Function to merge two issues, will create a new issue if source issue or
            destination issue is not a merged issue already.

            Will add new edges "merged_into" between the merged issue and the source
            issue and/or destination issue
            Will remove the "contains" edge between the project and the children issues
            of the new merged issue

        Args:
            project_uuid (str)
            source_issue (IssueResponse)
            destination_issue (IssueResponse)

        Returns:
            merged_issue (IssueResponse)
        """
        edge_repository = EdgeRepository(self.repository._client)
        # create merged_issue_data
        merged_issue_data = issue_merge(
            source_issue=source_issue, destination_issue=destination_issue
        )
        source_merged_check = edge_repository.read_in_edge_to_vertex(
            source_issue.uuid, "merged_into"
        )
        destination_merged_check = edge_repository.read_in_edge_to_vertex(
            destination_issue.uuid, "merged_into"
        )
        # TODO: what happens if they are both merged issues?
        if source_merged_check:
            parent_issue = self.update(
                issue_uuid=source_issue.uuid,
                modified_fields=merged_issue_data,
            )
            children_issue = [destination_issue]
        elif destination_merged_check:
            parent_issue = self.update(
                issue_uuid=destination_issue.uuid,
                modified_fields=merged_issue_data,
            )
            children_issue = [source_issue]
        else:
            parent_issue = self.create(
                project_uuid=project_uuid, issue_data=merged_issue_data
            )
            children_issue = [source_issue, destination_issue]

        for child_issue in children_issue:
            edge_repository.create(
                out_vertex_uuid=child_issue.uuid,
                in_vertex_uuid=parent_issue.uuid,
                edge_label="merged_into",
            )
            contains_edge = edge_repository.read_in_edge_to_vertex(
                vertex_uuid=child_issue.uuid, edge_label="contains"
            )
            edge_repository.delete(edge_uuid=contains_edge[0].uuid)

        return parent_issue

    def un_merge(self, project_uuid: str, merged_issue_uuid: str) -> list[str]:
        """Function to un-merge a merged issue

            Will create new "contains" edges for the parents of the merged issue
            Will remove the merged issue vertex

        Args:
            project_uuid (str)
            merged_issue_uuid (str)

        Returns:
            list[str]: uuids of the issues that had been merged
        """
        edge_repository = EdgeRepository(self.repository._client)
        # What if the merged_issue is not a merged issue? -> then the parent_issues
        # should be empty
        parent_issues = edge_repository.read_in_edge_to_vertex(
            merged_issue_uuid, "merged_into"
        )
        parent_issue_uuids = [issue.outV for issue in parent_issues]
        for parent_issue_uuid in parent_issue_uuids:
            edge_repository.create(
                out_vertex_uuid=project_uuid,
                in_vertex_uuid=parent_issue_uuid,
                edge_label="contains",
            )
        if len(parent_issue_uuids) > 0:
            self.repository.delete(merged_issue_uuid)
        return parent_issue_uuids
