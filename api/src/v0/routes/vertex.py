from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.client import DatabaseClient
from ..database.adapter import get_client
from ..models.filter import Filter
from ..models.vertex import VertexCreate, VertexResponse, VertexUpdate
from ..repositories.vertex import VertexRepository

router = APIRouter(
    tags=["vertex"],
    responses={404: {"description": "Not found"}},
    deprecated=False,
    include_in_schema=True,
)


@api_version(database_version)
@router.post(
    "/vertices/label/{vertex_label}",
    response_model=VertexResponse,
    summary="Create a new vertex by its label",
)
def create_vertex(
    vertex_label: str,
    vertex_data: VertexCreate,
    client: DatabaseClient = Depends(get_client),
):
    with client as c:
        return VertexRepository(c).create(
            vertex_label, VertexCreate.model_validate(vertex_data.model_dump())
        )


@api_version(database_version)
@router.get(
    "/vertices/label/{vertex_label}",
    response_model=list[VertexResponse],
    summary="Get all vertices by their label",
)
def read_vertex_all(vertex_label: str, client: DatabaseClient = Depends(get_client)):
    with client as c:
        return VertexRepository(c).all(vertex_label)


@api_version(database_version)
@router.get(
    "/vertices/{vertex_uuid}",
    response_model=VertexResponse,
    summary="Get a vertex by its UUID",
)
def read_vertex(vertex_uuid: str, client: DatabaseClient = Depends(get_client)):
    with client as c:
        return VertexRepository(c).read(vertex_uuid)


# dictionaries are difficult to use in the get request
# fix: provide filter dict as string and parse it as json to the repository function
# Example:
# http://localhost:8000/vertex/readallproject/49712919-cb6a-49a3-948a-d9e82aa9a5de?edge_label=contains&filter_dict={%22type%22:[%22uncertainty%22,%22decision%22,%22value%20metric%22]}
@api_version(database_version)
@router.get(
    "/vertices/{vertex_uuid}/children",
    response_model=list[VertexResponse],
    summary="Get the children of a vertex by its UUID",
)
def read_out_vertex(
    vertex_uuid: str,
    edge_label: str,
    filter_model: Filter = Depends(),
    original_vertex_label: str = None,
    client: DatabaseClient = Depends(get_client),
):
    with client as c:
        return VertexRepository(c).read_out_vertex(
            vertex_uuid=vertex_uuid,
            edge_label=edge_label,
            original_vertex_label=original_vertex_label,
            filter_model=filter_model,
        )


@api_version(database_version)
@router.get(
    "/vertices/{vertex_uuid}/parents",
    response_model=list[VertexResponse],
    summary="Get the parents of a vertex by its UUID",
)
def read_in_vertex(
    vertex_uuid: str,
    edge_label: str,
    filter_model: Filter = Depends(),
    original_vertex_label: str = None,
    client: DatabaseClient = Depends(get_client),
):
    with client as c:
        return VertexRepository(c).read_in_vertex(
            vertex_uuid=vertex_uuid,
            edge_label=edge_label,
            original_vertex_label=original_vertex_label,
            filter_model=filter_model,
        )


@api_version(database_version)
@router.patch(
    "/vertices/{vertex_uuid}",
    response_model=VertexResponse,
    summary="Delete a vertex by its UUID",
)
def update_vertex(
    vertex_uuid: str,
    modified_fields: VertexUpdate,
    client: DatabaseClient = Depends(get_client),
):
    with client as c:
        return VertexRepository(c).update(vertex_uuid, modified_fields)


@api_version(database_version)
@router.delete(
    "/vertices/{vertex_uuid}", response_model=None, summary="Delete a vertex by its UUID"
)
def delete_vertex(vertex_uuid: str, client: DatabaseClient = Depends(get_client)):
    with client as c:
        return VertexRepository(c).delete(vertex_uuid)
