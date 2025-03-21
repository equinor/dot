from unittest.mock import MagicMock

import pytest

from src.v0.database.gremlin import (
    Builder,
    GremlinClient,
    GremlinResponseBuilderEdge,
    GremlinResponseBuilderVertex,
    GremlinStringQueryBuilderEdge,
    GremlinStringQueryBuilderVertex,
    Query,
    Response,
)
from src.v0.models.objective import ObjectiveCreate, ObjectiveUpdate
from src.v0.repositories.objective import Filter, ObjectiveRepository


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
    mock_query.edge = GremlinStringQueryBuilderEdge()
    mock_response.vertex = GremlinResponseBuilderVertex()
    mock_response.edge = GremlinResponseBuilderEdge()

    # Set up the builder's query and response
    mock_builder.query = mock_query
    mock_builder.response = mock_response
    mock_client.builder = mock_builder

    return mock_client


@pytest.fixture
def objective():
    return {
        "description": ["an objective description"],
        "tag": ['["junk"]'],
        "index": ["1234"],
        "hierarchy": ["strategic"],
    }


@pytest.fixture
def metadata():
    return {
        "version": ["v0"],
        "uuid": ["1"],
        "timestamp": ["1234"],
        "date": ["today"],
        "T.id": "1",
        "T.label": "L",
    }


def test_read_success(mock_client, objective, metadata):
    body = [{**objective, **metadata}]
    mock_client.execute_query.return_value = body
    repository = ObjectiveRepository(mock_client)
    repository.read(objective_uuid="1")
    mock_client.execute_query.assert_called_once()


def test_read_objectives_all_success(mock_client, objective, metadata):
    body = [{**objective, **metadata}]
    mock_client.execute_query.return_value = body
    repository = ObjectiveRepository(mock_client)
    repository.read_objectives_all(
        project_uuid="0", vertex_label="V", edge_label="L", filter_model=Filter()
    )
    mock_client.execute_query.assert_called_once()


def test_create_success(mock_client, objective, metadata):
    body_vertex = [{**objective, **metadata}]
    body_edge = ["e[x][1-L->2]"]
    mock_client.execute_query.side_effect = [body_vertex, body_edge]
    repository = ObjectiveRepository(mock_client)
    repository.create(
        project_uuid="0",
        objective_data=ObjectiveCreate.model_validate(
            {
                "description": "an objective description",
                "tag": ["junk"],
                "index": "1234",
                "hierarchy": "fundamental",
            }
        ),
    )
    call_count = 1  # create objective vertex
    call_count += 1  # create edge to project
    assert mock_client.execute_query.call_count == call_count


def test_update_success(mock_client, objective, metadata):
    body = [{**objective, **metadata}]
    body[0]["description"] = ["A new one"]
    mock_client.execute_query.return_value = body
    repository = ObjectiveRepository(mock_client)
    repository.update(
        objective_uuid="1",
        modified_fields=ObjectiveUpdate(description="A new one"),
    )
    mock_client.execute_query.assert_called_once()


def test_delete_success(mock_client):
    mock_client.execute_query.return_value = None
    repository = ObjectiveRepository(mock_client)
    repository.delete(objective_uuid="1")
    call_count = 1  # delete all edges to project
    call_count += 1  # delete objective vertex
    assert mock_client.execute_query.call_count == call_count
