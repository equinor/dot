from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.gremlin import get_client
from ..models.filter import Filter
from ..models.objective import ObjectiveCreate, ObjectiveResponse, ObjectiveUpdate
from ..repositories.objective import ObjectiveRepository
from ..services.objective import ObjectiveService

router = APIRouter(
    tags=["objectives"],
    responses={404: {"description": "Not found"}},
    deprecated=False,
    include_in_schema=True,
)


def get_repository(client=Depends(get_client)):
    return ObjectiveRepository(client)


def get_service(repository=Depends(get_repository)):
    return ObjectiveService(repository)


@api_version(database_version)
@router.post(
    "/projects/{project_uuid}/objectives",
    response_model=ObjectiveResponse,
    summary="Create a new objective by its project UUID",
)
def create(
    project_uuid: str,
    objective_data: ObjectiveCreate,
    service: ObjectiveService = Depends(get_service),
) -> ObjectiveResponse:
    """Method to create a new objective connected to a project vertex

        Creates vertex with the label "objective" and the properties of
        objective_data
        Creates an edge between the project vertex specified by project_uuid
        and the newly create objective vertex

    Args:
        project_uuid (str): id of the project vertex the new objective will be
                            connected to
        objective_data (ObjectiveCreate): contains all properties for the objective

    Returns:
        ObjectiveResponse: Created Objective with the objective_data as
                            ObjectiveData
    """
    return service.create(project_uuid=project_uuid, objective_data=objective_data)


@api_version(database_version)
@router.get(
    "/projects/{project_uuid}/objectives",
    response_model=list[ObjectiveResponse],
    summary="Get all objectives by their project UUID",
)
def read_objectives_all(
    project_uuid: str,
    filter_model: Filter = Depends(),
    service: ObjectiveService = Depends(get_service),
) -> list[ObjectiveResponse]:
    """Read all objectives connected to one project with filter possibilities

    Args:
        project_uuid (str): id of the project vertex
        vertex_label (str): label of the vertices of interest
        edge_label (str): edge_label to clarify the connection between the project
                            node and objective node, should always be "contains" in
                            this method (default "contains")
        filter_model (Filter (BaseModel))
            contains a dict with different properties for filtering, like hierarchy,
            tag, and description

    Returns
        List[ObjectiveResponse]: List of Objectives which satisfy the condition to
                                    be connected to the Project vertex with a
                                    "contains" edge and have the label "objective" and
                                    satisfy the filters when the filter_model is given
    """
    return service.read_objectives_all(
        project_uuid=project_uuid,
        filter_model=filter_model,
    )


@api_version(database_version)
@router.get(
    "/objectives/{objective_uuid}",
    response_model=ObjectiveResponse,
    summary="Get an objective by its UUID",
)
def read(
    objective_uuid: str, service: ObjectiveService = Depends(get_service)
) -> ObjectiveResponse:
    """Method to read one objective based on the id

    Args:
        objective_uuid (str): id of the vertex with the label "objective"

    Returns
        ObjectiveResponse: Objective with all properties
    """
    return service.read(objective_uuid)


@api_version(database_version)
@router.patch(
    "/objectives/{objective_uuid}",
    response_model=ObjectiveResponse,
    summary="Partial update of an objective by its UUID",
)
def update_objective(
    objective_uuid: str,
    modified_fields: ObjectiveUpdate,
    service: ObjectiveService = Depends(get_service),
) -> ObjectiveResponse:
    """Updates the specified objective based on the id with the new objective_data

    Args:
        objective_uuid (str): id of the objective vertex
        modified_fields (ObjectiveUpdate): contains properties of the objective

    Returns:
        ObjectiveResponse: Objective with the objective_data as ObjectiveData
    """
    return service.update(objective_uuid, modified_fields)


@api_version(database_version)
@router.delete(
    "/objectives/{objective_uuid}",
    response_model=None,
    summary="Delete an objective by its UUID",
)
def delete_objective(
    objective_uuid: str, service: ObjectiveService = Depends(get_service)
):
    """Deletes the objective vertex based on the id and also all in and outgoing
        edges from this vertex

    Args:
        objective_uuid (str): id of the objective vertex

    Returns:
        None
    """
    service.delete(objective_uuid)
    return
