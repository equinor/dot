from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from src.authentication.auth import requires_role

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
    dependencies=[Depends(requires_role("DecisionOptimizationUser"))]

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
    """Method to create a new opportunity connected to a project vertex

        Creates vertex with the label "opportunity" and the properties of
        opportunity_data
        Creates an edge between the project vertex specified by project_uuid and the
        newly create opportunity vertex

    Args:
        project_uuid (str): id of the project vertex the new opportunity will be
                            connected to
        opportunity_data (OpportunityCreate): contains all properties for the
                                            opportunity

    Returns:
        OpportunityResponse: Created Opportunity with the opportunity_data as
        OpportunityCreate
    """
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
    """Read all opportunitys connected to one project with filter possibilities

    Args:
        project_uuid (str): id of the project vertex
        vertex_label (str): label of the vertices of interest
        edge_label (str):  edge_label to clarify the connection between the project
                            node and opportunity node, should always be "contains"
                            in this method (default "contains")
        filter_model (Filter(BaseModel)): contains a dict with different properties
                                            for filtering, like tag and description

    Returns
        List[OpportunityResponse]: List of Opportunitys which satisfy the condition
                                    to be connected to the Project vertex with a
                                    "contains" edge and have the label "opportunity"
                                    and satisfy the filters when the filter_model is
                                    given
    """
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
    """Read all opportunitys connected to one project with filter possibilities

    Args:
        project_uuid (str): id of the project vertex
        vertex_label (str): label of the vertices of interest
        edge_label (str):  edge_label to clarify the connection between the project
                            node and opportunity node, should always be "contains"
                            in this method (default "contains")
        filter_model (Filter(BaseModel)): contains a dict with different properties
                                            for filtering, like tag and description

    Returns
        List[OpportunityResponse]: List of Opportunitys which satisfy the condition
                                    to be connected to the Project vertex with a
                                    "contains" edge and have the label "opportunity"
                                    and satisfy the filters when the filter_model is
                                    given
    """
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
    """Updates the specified opportunity based on the id with the new
        opportunity_data

    Args:
        opportunity_uuid (str): id of the opportunity vertex
        modified_fields (OpportunityUpdate): contains properties of the opportunity

    Returns
        OpportunityResponse: Opportunity with the opportunity_data as
                                OpportunityData
    """
    return service.update(opportunity_uuid, modified_fields)


@api_version(database_version)
@router.delete(
    "/opportunities/{opportunity_uuid}",
    response_model=None,
    summary="Delete an objective by its UUID",
)
def delete(opportunity_uuid: str, service: OpportunityService = Depends(get_service)):
    """Deletes the opportunity vertex based on the id and also all in and outgoing
        edges from this vertex

    Args:
        opportunity_uuid (str): id of the opportunity vertex

    Returns
        None
    """
    return service.delete(opportunity_uuid)
