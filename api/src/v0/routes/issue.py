from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.adapter import get_client
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
    return service.update(issue_uuid, modified_fields)


@api_version(database_version)
@router.delete(
    "/issues/{issue_uuid}",
    response_model=None,
    summary="Delete an issue by its UUID",
)
def delete(issue_uuid: str, service: IssueService = Depends(get_service)):
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
):
    return service.un_merge(
        project_uuid=project_uuid, merged_issue_uuid=merged_issue_uuid
    )
