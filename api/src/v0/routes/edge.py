from fastapi import APIRouter, Depends, Query
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.gremlin import get_client
from ..models.edge import EdgeResponse
from ..repositories.edge import EdgeRepository
from ..services.edge import EdgeService

router = APIRouter(
    tags=["edges"],
    responses={404: {"description": "Not found"}},
    deprecated=False,
    include_in_schema=True,
)


def get_repository(client=Depends(get_client)):
    return EdgeRepository(client)


def get_service(repository=Depends(get_repository)):
    return EdgeService(repository)


@api_version(database_version)
@router.post(
    "/edges/label/{edge_label}",
    response_model=EdgeResponse,
    summary="Create a new edge by its label",
)
def create(
    out_vertex_uuid: str,
    in_vertex_uuid: str,
    edge_label: str,
    service: EdgeService = Depends(get_service),
) -> EdgeResponse:
    """Create a new edge between two vertices

    Args:
        out_vertex_uuid (str): id of the vertex where the edge goes out
        in_vertex_uuid (str): id of the vertex where the edge goes in
        edge_label (str): label of the edge ("contains" or "influences")

    Return:
        EdgeResponse: Edge (with properties id, outV, inV, uuid, label),
                        where id == uuid

    """
    return service.create(out_vertex_uuid, in_vertex_uuid, edge_label)


# TODO: Do we need this call?
@api_version(database_version)
@router.get(
    "/projects/{project_uuid}/edges/label/{edge_label}",
    response_model=list[EdgeResponse],
    summary="Get edges by their label from a project by its UUID",
)
def read_all_edges_from_project(
    project_uuid: str,
    edge_label: str,
    service: EdgeService = Depends(get_service),
) -> list[EdgeResponse]:
    """Method to return all edges with the specified edge label

    Args:
        project_uuid (str): id of the project vertex
        edge_label (str): label of the edge ("contains" or "influences")

    Returns:
        list[EdgeResponse]: List of Edges
    """
    return service.read_all_edges_from_project(project_uuid, edge_label)


# TODO: Do we need this call?
@api_version(database_version)
@router.get(
    "/project/{project_uuid}/edges/label/{edge_label}/vertices",
    response_model=list[EdgeResponse],
    summary=(
        "Get edges by their label and their heads and "
        "tails from a project by its UUID"
    ),
)
def read_all_edges_from_sub_project(
    project_uuid: str,
    edge_label: str,
    vertex_uuid: list[str] = Query(None),
    service: EdgeService = Depends(get_service),
) -> list[EdgeResponse]:
    """Method to return all edges with the specified edge label and linking vertices
        with given properties

    Args:
        project_uuid (str): id of the project vertex
        edge_label (str): label of the edge ("contains" or "influences")
        vertex_uuid (list[str]): list of vertices uuid of the sub-project

    Returns:
        list[EdgeResponse]: List of Edges
    """
    return service.read_all_edges_from_sub_project(project_uuid, edge_label, vertex_uuid)


@api_version(database_version)
@router.get(
    "/vertices/{vertex_uuid}/edges/label/{edge_label}/outgoing",
    response_model=list[EdgeResponse],
    summary=(
        "Get outgoing edges by their label and " "their heads from a project by its UUID"
    ),
)
def read_out_edge_from_vertex(
    vertex_uuid: str,
    edge_label: str,
    service: EdgeService = Depends(get_service),
) -> list[EdgeResponse]:
    """Returns edges going out of the specified vertex

    Args:
        vertex_uuid (str): id of the vertex
        edge_label (str): label of the edge
    Return:
        List of edges
    """
    return service.read_out_edge_from_vertex(vertex_uuid, edge_label)


@api_version(database_version)
@router.get(
    "/vertices/{vertex_uuid}/edges/label/{edge_label}/incoming",
    response_model=list[EdgeResponse],
    summary=(
        "Get incoming edges by their label and " "their tails from a project by its UUID"
    ),
)
def read_in_edge_to_vertex(
    vertex_uuid: str,
    edge_label: str,
    service: EdgeService = Depends(get_service),
) -> list[EdgeResponse]:
    """Returns edges going in to the specified vertex

    Args:
        vertex_uuid (str): id of the vertex
        edge_label (str): label of the edge
    Return:
        List of edges
    """
    return service.read_in_edge_to_vertex(vertex_uuid, edge_label)


# TODO: Do we need this call?
@api_version(database_version)
@router.get(
    "/edges/{edge_id}",
    response_model=EdgeResponse,
    summary="Get an edge by its UUID",
)
def read(edge_id: str, service: EdgeService = Depends(get_service)) -> EdgeResponse:
    """Method to read one edge based on the id

    Args:
        edge_uuid (str): id of the edge

    Returns:
        EdgeResponse: Edge
    """
    return service.read(edge_id)


# # TODO: Do we need this call?
# @api_version(database_version)
# @router.patch(
#     "/edges/{edge_id}",
#     response_model=EdgeResponse,
#     summary="Update an edge by its UUID",
# )
# def update(
#     edge_id: str,
#     modified_fields: EdgeUpdate,
#     service: EdgeService = Depends(get_service),
# ):
#     return service.update(edge_id, modified_fields)


@api_version(database_version)
@router.delete(
    "/edges/{edge_id}",
    response_model=None,
    summary="Delete an edge by its UUID",
)
def delete(edge_id: str, service: EdgeService = Depends(get_service)) -> None:
    """Deletes edges going in and out of the specified vertex

    Args:
        vertex_uuid (str): id of the vertex

    Return:
        None
    """
    return service.delete(edge_id)


# TODO: add more routers for special deletion of edges based on vertices.
