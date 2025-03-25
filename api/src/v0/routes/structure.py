from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.adapter import get_client
from ..models.structure import DecisionTreeResponse, InfluenceDiagramResponse
from ..repositories.vertex import VertexRepository
from ..services.structure import StructureService

router = APIRouter(
    tags=["structures"],
    responses={404: {"description": "Not found"}},
    deprecated=False,
    include_in_schema=True,
)


def get_repository(client=Depends(get_client)):
    return VertexRepository(client)


def get_service(repository=Depends(get_repository)):
    return StructureService(repository)


@api_version(database_version)
@router.get(
    "/projects/{project_uuid}/influence-diagram",
    response_model=InfluenceDiagramResponse,
    summary="Get the influence diagram from project by its UUID",
)
def read_influence_diagram(
    project_uuid: str, service: StructureService = Depends(get_service)
):
    return service.read_influence_diagram(project_uuid=project_uuid)


@api_version(database_version)
@router.get(
    "/projects/{project_uuid}/decision-tree",
    response_model=DecisionTreeResponse,
    summary="Get the decision tree from project by its UUID",
)
def convert_influence_diagram_to_decision_tree_model(
    project_uuid: str, service: StructureService = Depends(get_service)
):
    return service.create_decision_tree(project_uuid=project_uuid)
