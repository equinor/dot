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
from src.v0.models.opportunity import OpportunityCreate, OpportunityUpdate
from src.v0.repositories.opportunity import Filter, OpportunityRepository
from src.v0.services.opportunity import OpportunityService


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
    mock_repository = MagicMock(spec=OpportunityRepository)
    service = OpportunityService(mock_client)
    service.repository = mock_repository

    service.create(
        project_uuid="1",
        opportunity_data=OpportunityCreate(
            description="A description", tag=["tag1", "tag2"]
        ),
    )
    mock_repository.create.assert_called_once()


def test_read_opportunities_all_success(mock_client):
    mock_repository = MagicMock(spec=OpportunityRepository)
    service = OpportunityService(mock_client)
    service.repository = mock_repository

    service.read_opportunities_all(
        project_uuid="1",
        filter_model=Filter(),
    )
    mock_repository.read_opportunities_all.assert_called_once()


def test_read_success(mock_client):
    mock_repository = MagicMock(spec=OpportunityRepository)
    service = OpportunityService(mock_client)
    service.repository = mock_repository

    service.read(opportunity_uuid="1")
    mock_repository.read.assert_called_once()


def test_update_success(mock_client):
    mock_repository = MagicMock(spec=OpportunityRepository)
    service = OpportunityService(mock_client)
    service.repository = mock_repository

    service.update(
        opportunity_uuid="1", modified_fields=OpportunityUpdate(description="D")
    )
    mock_repository.update.assert_called_once()


def test_delete_success(mock_client):
    mock_repository = MagicMock(spec=OpportunityRepository)
    service = OpportunityService(mock_client)
    service.repository = mock_repository

    service.delete(opportunity_uuid="1")
    mock_repository.delete.assert_called_once()
