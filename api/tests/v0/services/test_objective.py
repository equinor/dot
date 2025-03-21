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
from src.v0.services.objective import ObjectiveService


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


def test_create_success(mock_client):
    mock_repository = MagicMock(spec=ObjectiveRepository)
    service = ObjectiveService(mock_client)
    service.repository = mock_repository

    service.create(
        project_uuid="1",
        objective_data=ObjectiveCreate(
            description="A description", tag=["tag1", "tag2"]
        ),
    )
    mock_repository.create.assert_called_once()


def test_read_objectives_all_success(mock_client):
    mock_repository = MagicMock(spec=ObjectiveRepository)
    service = ObjectiveService(mock_client)
    service.repository = mock_repository

    service.read_objectives_all(
        project_uuid="1",
        filter_model=Filter(),
    )
    mock_repository.read_objectives_all.assert_called_once()


def test_read_success(mock_client):
    mock_repository = MagicMock(spec=ObjectiveRepository)
    service = ObjectiveService(mock_client)
    service.repository = mock_repository

    service.read(objective_uuid="1")
    mock_repository.read.assert_called_once()


def test_update_success(mock_client):
    mock_repository = MagicMock(spec=ObjectiveRepository)
    service = ObjectiveService(mock_client)
    service.repository = mock_repository

    service.update(objective_uuid="1", modified_fields=ObjectiveUpdate(description="D"))
    mock_repository.update.assert_called_once()


def test_delete_success(mock_client):
    mock_repository = MagicMock(spec=ObjectiveRepository)
    service = ObjectiveService(mock_client)
    service.repository = mock_repository

    service.delete(objective_uuid="1")
    mock_repository.delete.assert_called_once()
