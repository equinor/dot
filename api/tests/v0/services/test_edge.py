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
from src.v0.services.edge import EdgeService


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


def test_create_success(mock_client):
    mock_repository = MagicMock(spec=EdgeRepository)
    service = EdgeService(mock_client)
    service.repository = mock_repository

    service.create(out_vertex_uuid="1", in_vertex_uuid="2", edge_label="L")
    mock_repository.create.assert_called_once()


def test_read_all_edges_from_project_success(mock_client):
    mock_repository = MagicMock(spec=EdgeRepository)
    service = EdgeService(mock_client)
    service.repository = mock_repository

    service.read_all_edges_from_project(project_uuid="1", edge_label="L")
    mock_repository.read_all_edges_from_project.assert_called_once()


def test_read_all_edges_from_sub_project_success(mock_client):
    mock_repository = MagicMock(spec=EdgeRepository)
    service = EdgeService(mock_client)
    service.repository = mock_repository

    service.read_all_edges_from_sub_project(
        project_uuid="1", edge_label="L", vertex_uuid=["5", "7"]
    )
    mock_repository.read_all_edges_from_sub_project.assert_called_once()


def test_read_out_edge_from_vertex_success(mock_client):
    mock_repository = MagicMock(spec=EdgeRepository)
    service = EdgeService(mock_client)
    service.repository = mock_repository

    service.read_out_edge_from_vertex(vertex_uuid="1", edge_label="L")
    mock_repository.read_out_edge_from_vertex.assert_called_once()


def test_read_in_edge_to_vertex_success(mock_client):
    mock_repository = MagicMock(spec=EdgeRepository)
    service = EdgeService(mock_client)
    service.repository = mock_repository

    service.read_in_edge_to_vertex(vertex_uuid="1", edge_label="L")
    mock_repository.read_in_edge_to_vertex.assert_called_once()


def test_read_success(mock_client):
    mock_repository = MagicMock(spec=EdgeRepository)
    service = EdgeService(mock_client)
    service.repository = mock_repository

    service.read(edge_uuid="1")
    mock_repository.read.assert_called_once()


# def test_update_success(mock_client):
#     mock_repository = MagicMock(spec=EdgeRepository)
#     service = EdgeService(mock_client)
#     service.repository = mock_repository

#     service.update(edge_uuid="1", edge_data=EdgeUpdate(inV="3"))
#     mock_repository.update.assert_called_once()


def test_delete_success(mock_client):
    mock_repository = MagicMock(spec=EdgeRepository)
    service = EdgeService(mock_client)
    service.repository = mock_repository

    service.delete(edge_uuid="1")
    mock_repository.delete.assert_called_once()
