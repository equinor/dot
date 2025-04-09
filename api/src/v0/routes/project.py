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
    """Method to create a new project vertex

        Creates vertex with the label "project" and the properties of project_data

    Args:
        project_data (ProjectCreate): contains all properties for the project

    Returns
        ProjectResponse: Created Project with the project_data as ProjectCreate
    """
    return service.create(project_data)


@api_version(database_version)
@router.get(
    "/projects", response_model=list[ProjectResponse], summary="Read all projects"
)
def read_projects_all(
    service: ProjectService = Depends(get_service),
) -> list[ProjectResponse]:
    """Reads all project vertices

    Args:
        None

    Returns
        List[ProjectResponse]: List of Projects in the database
    """
    return service.read_projects_all()


@api_version(database_version)
@router.get(
    "/projects/{project_uuid}", response_model=ProjectResponse, summary="Read a project"
)
def read(
    project_uuid: str, service: ProjectService = Depends(get_service)
) -> ProjectResponse:
    """Method to read one project based on the id

    Args:
        project_uuid (str): id of the vertex with the label "project"'

    Returns
        ProjectResponse: Project with all properties
    """
    return service.read(project_uuid)


@api_version(database_version)
@router.get(
    "/projects/{project_uuid}/export", response_model=dict, summary="Export a project"
)
def export_project(
    project_uuid: str, service: ProjectService = Depends(get_service)
) -> dict:
    """Method to export one project based on the id in JSON format

    Args
        project_uuid (str): id of the vertex with the label "project"'

    Returns
        json_dict: JSON dictionary containing the project data
    """
    return service.export_project(project_uuid)


@api_version(database_version)
@router.post("/projects/import", response_model=None, summary="Import a project")
def import_project(
    project_json: dict, service: ProjectService = Depends(get_service)
) -> None:
    """Method to import a project in JSON format

    Args:
        project_json (dict): JSON dictionary with the project data

    Returns
        None
    """
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
    """Updates the specified project based on the id with the new project_data

    Args:
        project_uuid (str): id of the project vertex
        modified_fields (ProjectUpdate): contains properties of the project

    Returns
        ProjectResponse: Project with the project_data as ProjectUpdate
    """
    return service.update(project_uuid, modified_fields)


@api_version(database_version)
@router.delete(
    "/projects/{project_uuid}", response_model=None, summary="Delete a project"
)
def delete(project_uuid: str, service: ProjectService = Depends(get_service)) -> None:
    """Gets all vertices connected (via edge with label "contains") to the project
            vertex with the id = project_uuid

        Deletes all edges from these vertices and deletes afterwards all vertices
        connected to the project
        Deletes the project vertex based on the id

    Args
        project_uuid (str): id of the project vertex

    Returns
        None
    """
    return service.delete(project_uuid)
