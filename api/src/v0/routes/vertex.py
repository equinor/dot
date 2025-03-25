from fastapi import APIRouter, Depends
from fastapi_versionizer.versionizer import api_version

from .. import database_version
from ..database.client import DatabaseClient
from ..database.gremlin import get_client
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
) -> VertexResponse:
    """Creates a new vertex based on vertex data

    Args:
        vertex_label (str): given vertex label for gremlin DB, e.g. "issue",
                            "project", "opportunity", "objective"
        vertex (VertexCreate): data for properties in vertex
            provides generated uuid
            provides uuid will also be set as the id in the DB

    Return:
        VertexResponse: dict of the created vertex

    """
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
def read_vertex_all(
    vertex_label: str, client: DatabaseClient = Depends(get_client)
) -> list[VertexResponse]:
    """Read all vertices given a label

    Args:
        vertex_label (str): label of vertices to read (e.g. opportunity)

    Returns:
        list[VertexResponse]: list of vertices with the given label
    """
    with client as c:
        return VertexRepository(c).all(vertex_label)


@api_version(database_version)
@router.get(
    "/vertices/{vertex_uuid}",
    response_model=VertexResponse,
    summary="Get a vertex by its UUID",
)
def read_vertex(
    vertex_uuid: str, client: DatabaseClient = Depends(get_client)
) -> VertexResponse:
    """Reads a vertex based on the vertex id in the DB

    Args:
        vertex_uuid (str): uuid of the vertex.

            uuid property [g.V().property("uuid",...)] and vertex id [g.V(id)] are
            the same based on the implementation in the create method
            This is an active choice of us, otherwise, the id will be automatically
            generated in the DB

    Return:
        VertexResponse: dict with all data of the vertex (VertexResponse)
    """
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
) -> list[VertexResponse]:
    """Read vertices based on outgoing edge labels.

    Args:
        vertex_uuid (str): id of the vertex
        edge_label (str): edge label, e.g. "contains" or "influences"
        original_vertex_label (str, optional): label of the vertices we are
                                                interested in (e.g. only issues or
                                                also opportunities and objectives).
                                                Defaults to None.
        filter_model (Filter, optional): BaseModel containing properties to use as
                                            a filter, for example the type or tag of
                                            vertices. Defaults to None.

    Returns:
        List[VertexResponse]:
            List of all vertices connected to the vertex with the vertex id
            vertex_uuid through an edge with the label edge_label
            When original_vertex_label is given the vertices will be filtered
            based on the label of the vertex, e.g. it will return either "issue",
            "opportunity" or "objective" vertices otherwise, all vertices are
            returned
            When filter_model is given, the vertices will be filtered based on the
            content of the filter model. Currently this can be "tag", "type",...
            and other properties of the vertices defined in the database
            If filter_model is None, no filter will be applied and all vertices will
            be returned.
    """
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
) -> list[VertexResponse]:
    """Read vertices based on incoming edge labels.

    Args:
        vertex_uuid (str): id of the vertex
        edge_label (str): edge label, e.g. "contains" or "influences"
        original_vertex_label (str, optional): label of the vertices we are
                                                interested in (e.g. only issues or
                                                also opportunities and objectives).
                                                Defaults to None.
        filter_model (Filter, optional): BaseModel containing properties to use
                                            as a filter, for example the type or tag
                                            of vertices. Defaults to None.

    Returns:
        List[VertexResponse]: List of all vertices connected to the vertex with
                                the vertex id vertex_uuid through an incoming edge
                                with the label edge_label

            When original_vertex_label is given, the vertices will be filtered
            based on the label of the vertex, e.g. it will return either "issue",
            "opportunity" or "objective" vertices. Otherwise, all vertices are
            returned.
            When filter_model is given, the vertices will be filtered based on
            the content of the filter model. Currently, this can be "tag", "type",
            and other properties of the vertices defined in the database.
            If filter_model is None, no filter will be applied and all vertices will
            be returned.
    """
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
) -> VertexResponse:
    """Updated the specified vertex with the new vertex properties

    Args:
        vertex_uuid (str): id of the to be updated vertex
        modified_fields (VertexUpdate): properties of vertices which will
                                        be updated

    Return:
        VertexResponse: vertex dict with updated properties
    """
    with client as c:
        return VertexRepository(c).update(vertex_uuid, modified_fields)


@api_version(database_version)
@router.delete(
    "/vertices/{vertex_uuid}", response_model=None, summary="Delete a vertex by its UUID"
)
def delete_vertex(
    vertex_uuid: str, client: DatabaseClient = Depends(get_client)
) -> None:
    """method to delete a vertex based on the vertex id

    Args:
        vertex_uuid (str): id of the vertex which will be deleted

    Return:
        None
    """
    with client as c:
        return VertexRepository(c).delete(vertex_uuid)
