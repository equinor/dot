from unittest.mock import MagicMock

import pytest

from src.v0.database.gremlin import (
    Builder,
    GremlinClient,
    GremlinResponseBuilderVertex,
    GremlinStringQueryBuilderVertex,
    Query,
    Response,
)
from src.v0.models.vertex import VertexCreate, VertexUpdate
from src.v0.repositories.vertex import VertexRepository


@pytest.fixture
def mock_client():
    # Create a mock client
    mock_client = MagicMock(spec=GremlinClient)
    mock_client.__enter__.return_value = mock_client

    # Create mock builder and its components
    mock_builder = MagicMock(spec=Builder)
    mock_query = MagicMock(spec=Query)
    mock_response = MagicMock(spec=Response)
    mock_query.vertex = GremlinStringQueryBuilderVertex()
    mock_response.vertex = GremlinResponseBuilderVertex()

    # Set up the builder's query and response
    mock_builder.query = mock_query
    mock_builder.response = mock_response
    mock_client.builder = mock_builder

    return mock_client


@pytest.fixture
def metadata():
    return {
        "version": ["v0"],
        "uuid": ["1"],
        "timestamp": ["1234"],
        "date": ["today"],
        "T.id": "1",
    }


def test_create_success(mock_client, metadata):
    response = [{**{"field": ["3"], "T.label": "V"}, **metadata}]
    mock_client.execute_query.return_value = response
    repository = VertexRepository(mock_client)
    repository.create(vertex_label="L", vertex=VertexCreate(field="3"))
    mock_client.execute_query.assert_called_once()


def test_read_success(mock_client, metadata):
    response = [{**{"field": ["3"], "T.label": "V"}, **metadata}]
    mock_client.execute_query.return_value = response
    repository = VertexRepository(mock_client)
    repository.read(vertex_uuid="1")
    mock_client.execute_query.assert_called_once()


def test_read_out_vertex_success(mock_client, metadata):
    response = [{**{"field": ["3"], "T.label": "V"}, **metadata}]
    mock_client.execute_query.return_value = response
    repository = VertexRepository(mock_client)
    repository.read_out_vertex(vertex_uuid="1", edge_label="V")
    mock_client.execute_query.assert_called_once()


def test_read_in_vertex_success(mock_client, metadata):
    response = [{**{"field": ["3"], "T.label": "V"}, **metadata}]
    mock_client.execute_query.return_value = response
    repository = VertexRepository(mock_client)
    repository.read_in_vertex(vertex_uuid="1", edge_label="V")
    mock_client.execute_query.assert_called_once()


def test_all_success(mock_client, metadata):
    response = [{**{"field": ["3"], "T.label": "V"}, **metadata}]
    mock_client.execute_query.return_value = response
    repository = VertexRepository(mock_client)
    repository.all(vertex_label="V")
    mock_client.execute_query.assert_called_once()


def test_update_success(mock_client, metadata):
    response = [{**{"field": ["4"], "T.label": "V"}, **metadata}]
    mock_client.execute_query.return_value = response
    repository = VertexRepository(mock_client)
    repository.update(vertex_uuid="1", modified_fields=VertexUpdate(field=4))
    mock_client.execute_query.assert_called_once()


def test_delete_success(mock_client, metadata):
    response = [{None}]
    mock_client.execute_query.return_value = response
    repository = VertexRepository(mock_client)
    repository.delete(vertex_uuid="1")
    mock_client.execute_query.assert_called_once()
