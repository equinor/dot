from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.adapter import get_client
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
    service.delete(objective_uuid)
    return
