from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.adapter import get_client
from ..models.project import ProjectCreate, ProjectResponse, ProjectUpdate
from ..repositories.project import ProjectRepository
from ..services.project import ProjectService

router = APIRouter(
    tags=["projects"],
    responses={404: {"description": "Not found"}},
    deprecated=False,
    include_in_schema=True,
)


def get_repository(client=Depends(get_client)):
    return ProjectRepository(client)


def get_service(repository=Depends(get_repository)):
    return ProjectService(repository)


@api_version(database_version)
@router.post("/projects", response_model=ProjectResponse, summary="Create a new project")
def create(
    project_data: ProjectCreate, service: ProjectService = Depends(get_service)
) -> ProjectResponse:
    return service.create(project_data)


@api_version(database_version)
@router.get(
    "/projects", response_model=list[ProjectResponse], summary="Read all projects"
)
def read_projects_all(
    service: ProjectService = Depends(get_service),
) -> list[ProjectResponse]:
    return service.read_projects_all()


@api_version(database_version)
@router.get(
    "/projects/{project_uuid}", response_model=ProjectResponse, summary="Read a project"
)
def read(
    project_uuid: str, service: ProjectService = Depends(get_service)
) -> ProjectResponse:
    return service.read(project_uuid)


@api_version(database_version)
@router.get("/projects/{project_uuid}/export", summary="Export a project")
def export_project(project_uuid: str, service: ProjectService = Depends(get_service)):
    return service.export_project(project_uuid)


@api_version(database_version)
@router.post("/projects/import", summary="Import a project")
def import_project(project_json: dict, service: ProjectService = Depends(get_service)):
    return service.import_project(project_json)


@api_version(database_version)
@router.patch(
    "/projects/{project_uuid}",
    response_model=ProjectResponse,
    summary="Update a project",
)
def update(
    project_uuid: str,
    modified_fields: ProjectUpdate,
    service: ProjectService = Depends(get_service),
) -> ProjectResponse:
    return service.update(project_uuid, modified_fields)


@api_version(database_version)
@router.delete("/projects/{project_uuid}", summary="Delete a project")
def delete(project_uuid: str, service: ProjectService = Depends(get_service)):
    return service.delete(project_uuid)
