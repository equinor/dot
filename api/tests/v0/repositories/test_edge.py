from unittest.mock import MagicMock

import pytest

from src.v0.database.gremlin import (
    Builder,
    GremlinClient,
    GremlinResponseBuilderEdge,
    GremlinStringQueryBuilderEdge,
    Query,
    Response,
)
from src.v0.repositories.edge import EdgeRepository


@pytest.fixture
def mock_client():
    # Create a mock client
    mock_client = MagicMock(spec=GremlinClient)
    mock_client.__enter__.return_value = mock_client

    # Create mock builder and its components
    mock_builder = MagicMock(spec=Builder)
    mock_query = MagicMock(spec=Query)
    mock_response = MagicMock(spec=Response)
    mock_query.edge = GremlinStringQueryBuilderEdge()
    mock_response.edge = GremlinResponseBuilderEdge()

    # Set up the builder's query and response
    mock_builder.query = mock_query
    mock_builder.response = mock_response
    mock_client.builder = mock_builder

    return mock_client


def test_read_all_edges_from_project_success(mock_client):
    mock_client.execute_query.return_value = ["e[x][1-L->2]"]
    repository = EdgeRepository(mock_client)
    repository.read_all_edges_from_project(project_uuid="0", edge_label="L")
    mock_client.execute_query.assert_called_once()


def test_read_all_edges_from_sub_project_success(mock_client):
    mock_client.execute_query.return_value = ["e[x][1-L->2]"]
    repository = EdgeRepository(mock_client)
    repository.read_all_edges_from_sub_project(
        project_uuid="0", edge_label="L", vertex_uuid="1"
    )
    mock_client.execute_query.assert_called_once()


def test_create_success(mock_client):
    mock_client.execute_query.return_value = ["e[x][1-L->2]"]
    repository = EdgeRepository(mock_client)
    repository.create(out_vertex_uuid="1", in_vertex_uuid="2", edge_label="L")
    mock_client.execute_query.assert_called_once()


def test_read_out_edge_from_vertex_success(mock_client):
    mock_client.execute_query.return_value = ["e[x][1-L->2]"]
    repository = EdgeRepository(mock_client)
    repository.read_out_edge_from_vertex(vertex_uuid="1", edge_label="L")
    mock_client.execute_query.assert_called_once()


def test_read_in_edge_to_vertex_success(mock_client):
    mock_client.execute_query.return_value = ["e[x][1-L->2]"]
    repository = EdgeRepository(mock_client)
    repository.read_in_edge_to_vertex(vertex_uuid="1", edge_label="L")
    mock_client.execute_query.assert_called_once()


def test_read_success(mock_client):
    mock_client.execute_query.return_value = ["e[x][1-L->2]"]
    repository = EdgeRepository(mock_client)
    repository.read(edge_uuid="1")
    mock_client.execute_query.assert_called_once()


# def test_update_success(mock_client):
#     mock_client.execute_query.return_value = ["e[x][1-L->2]"]
#     repository = EdgeRepository(mock_client)
#     repository.update(edge_uuid="1", modified_fields=EdgeUpdate(inV="2"))
#     mock_client.execute_query.assert_called_once()


def test_delete_success(mock_client):
    mock_client.execute_query.return_value = None
    repository = EdgeRepository(mock_client)
    repository.delete(edge_uuid="1")
    mock_client.execute_query.assert_called_once()


def test_delete_edge_from_vertex_success(mock_client):
    mock_client.execute_query.return_value = None
    repository = EdgeRepository(mock_client)
    repository.delete_edge_from_vertex(vertex_uuid="1")
    mock_client.execute_query.assert_called_once()
