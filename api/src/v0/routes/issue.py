from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.gremlin import get_client
from ..models.filter import Filter
from ..models.issue import IssueCreate, IssueResponse, IssueUpdate
from ..repositories.issue import IssueRepository
from ..services.issue import IssueService

router = APIRouter(
    tags=["issues"],
    responses={404: {"description": "Not found"}},
    deprecated=False,
    include_in_schema=True,
)


def get_repository(client=Depends(get_client)):
    return IssueRepository(client)


def get_service(repository=Depends(get_repository)):
    return IssueService(repository)


@api_version(database_version)
@router.post(
    "/projects/{project_uuid}/issues",
    response_model=IssueResponse,
    summary="Create a new issue by its project UUID",
)
def create(
    project_uuid: str,
    issue_data: IssueCreate,
    service: IssueService = Depends(get_service),
) -> IssueResponse:
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
    return service.create(project_uuid=project_uuid, issue_data=issue_data)


@api_version(database_version)
@router.get(
    "/projects/{project_uuid}/issues",
    response_model=list[IssueResponse],
    summary="Get all issues by their project UUID",
)
def read_issues_all(
    project_uuid: str,
    filter_model: Filter = Depends(),
    service: IssueService = Depends(get_service),
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
    return service.read_issues_all(
        project_uuid=project_uuid,
        filter_model=filter_model,
    )


@api_version(database_version)
@router.get(
    "/issues/{issue_uuid}",
    response_model=IssueResponse,
    summary="Get an issue by its UUID",
)
def read(
    issue_uuid: str,
    service: IssueService = Depends(get_service),
) -> IssueResponse:
    """Method to read one issue based on the id

    Args:
        issue_uuid (str): id of the vertex with the label "issue"

    Returns:
        IssueResponse: Issue with all properties
    """
    return service.read(issue_uuid)


@api_version(database_version)
@router.patch(
    "/issues/{issue_uuid}",
    response_model=IssueResponse,
    summary="Partial update of an issue by its UUID",
)
def update(
    issue_uuid: str,
    modified_fields: IssueUpdate,
    service: IssueService = Depends(get_service),
) -> IssueResponse:
    """Updates the specified issue based on the id with the new issue_data

    Args:
        issue_uuid (str): id of the issue vertex
        modified_fields (IssueUpdate): contains properties of the issue

    Returns:
        IssueResponse: Issue with the issue_data as IssueCreate
    """
    return service.update(issue_uuid, modified_fields)


@api_version(database_version)
@router.delete(
    "/issues/{issue_uuid}",
    response_model=None,
    summary="Delete an issue by its UUID",
)
def delete(issue_uuid: str, service: IssueService = Depends(get_service)) -> None:
    """Deletes the issue vertex based on the id and also all in and outgoing edges
        from this vertex

    Args:
        issue_uuid (str): id of the issue vertex

    Returns:
        None
    """
    service.delete(issue_uuid)
    return


@api_version(database_version)
@router.post(
    "/projects/{project_uuid}/merge",
    response_model=IssueResponse,
    summary="Merged 2 issues within a project by its UUID",
)
def merge(
    project_uuid: str,
    source_issue: IssueResponse,
    destination_issue: IssueResponse,
    service: IssueService = Depends(get_service),
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
    return service.merge(
        project_uuid=project_uuid,
        source_issue=source_issue,
        destination_issue=destination_issue,
    )


@api_version(database_version)
@router.post(
    "/projects/{project_uuid}/un-merge/issues/{merged_issue_uuid}",
    response_model=list[str],
    summary="Unmerge a merged issue by its UUID within a project by its UUID",
)
def un_merge(
    project_uuid: str,
    merged_issue_uuid: str,
    service: IssueService = Depends(get_service),
) -> list[str]:
    """Function to un-merge a merged issue

        Will create new "contains" edges for the parents of the merged issue
        Will remove the merged issue vertex

    Args:
        project_uuid (str)
        merged_issue_uuid (str)

    Returns:
        list[str]: uuids of the issues that had been merged
    """
    return service.un_merge(
        project_uuid=project_uuid, merged_issue_uuid=merged_issue_uuid
    )
