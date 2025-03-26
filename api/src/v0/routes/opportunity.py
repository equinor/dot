from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.adapter import get_client
from ..models.filter import Filter
from ..models.opportunity import (
    OpportunityCreate,
    OpportunityResponse,
    OpportunityUpdate,
)
from ..repositories.opportunity import OpportunityRepository
from ..services.opportunity import OpportunityService

router = APIRouter(
    tags=["opportunities"],
    responses={404: {"description": "Not found"}},
    deprecated=False,
    include_in_schema=True,
)


def get_repository(client=Depends(get_client)):
    return OpportunityRepository(client)


def get_service(repository=Depends(get_repository)):
    return OpportunityService(repository)


@api_version(database_version)
@router.post(
    "/projects/{project_uuid}/opportunities",
    response_model=OpportunityResponse,
    summary="Create a new opportunity by its project UUID",
)
def create(
    project_uuid: str,
    opportunity_data: OpportunityCreate,
    service: OpportunityService = Depends(get_service),
) -> OpportunityResponse:
    return service.create(project_uuid=project_uuid, opportunity_data=opportunity_data)


@api_version(database_version)
@router.get(
    "/projects/{project_uuid}/opportunities",
    response_model=list[OpportunityResponse],
    summary="Get all opportunities by their project UUID",
)
def read_opportunities_all(
    project_uuid: str,
    filter_model: Filter = Depends(),
    service: OpportunityService = Depends(get_service),
) -> list[OpportunityResponse]:
    return service.read_opportunities_all(
        project_uuid=project_uuid,
        filter_model=filter_model,
    )


@api_version(database_version)
@router.get(
    "/opportunities/{opportunity_uuid}",
    response_model=OpportunityResponse,
    summary="Get an opportunity by its UUID",
)
def read(opportunity_uuid: str, service: OpportunityService = Depends(get_service)):
    return service.read(opportunity_uuid)


@api_version(database_version)
@router.patch(
    "/opportunities/{opportunity_uuid}",
    response_model=OpportunityResponse,
    summary="Partial update of an opportunity by its UUID",
)
def update(
    opportunity_uuid: str,
    modified_fields: OpportunityUpdate,
    service: OpportunityService = Depends(get_service),
):
    return service.update(opportunity_uuid, modified_fields)


@api_version(database_version)
@router.delete(
    "/opportunities/{opportunity_uuid}",
    response_model=None,
    summary="Delete an objective by its UUID",
)
def delete(opportunity_uuid: str, service: OpportunityService = Depends(get_service)):
    return service.delete(opportunity_uuid)
