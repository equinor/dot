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
def opportunity():
    return {
        "description": ["an opportunity description"],
        "tag": ['["junk"]'],
        "index": ["1234"],
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


def test_read_success(mock_client, opportunity, metadata):
    body = [{**opportunity, **metadata}]
    mock_client.execute_query.return_value = body
    repository = OpportunityRepository(mock_client)
    repository.read(opportunity_uuid="1")
    mock_client.execute_query.assert_called_once()


def test_read_opportunities_all_success(mock_client, opportunity, metadata):
    body = [{**opportunity, **metadata}]
    mock_client.execute_query.return_value = body
    repository = OpportunityRepository(mock_client)
    repository.read_opportunities_all(
        project_uuid="0", vertex_label="V", edge_label="L", filter_model=Filter()
    )
    mock_client.execute_query.assert_called_once()


def test_create_success(mock_client, opportunity, metadata):
    body_vertex = [{**opportunity, **metadata}]
    body_edge = ["e[x][1-L->2]"]
    mock_client.execute_query.side_effect = [body_vertex, body_edge]
    repository = OpportunityRepository(mock_client)
    repository.create(
        project_uuid="0",
        opportunity_data=OpportunityCreate.model_validate(
            {
                "description": "an opportunity description",
                "tag": ["junk"],
                "index": "1234",
            }
        ),
    )
    call_count = 1  # create opportunity vertex
    call_count += 1  # create edge to project
    assert mock_client.execute_query.call_count == call_count


def test_update_success(mock_client, opportunity, metadata):
    body = [{**opportunity, **metadata}]
    body[0]["description"] = ["A new one"]
    mock_client.execute_query.return_value = body
    repository = OpportunityRepository(mock_client)
    repository.update(
        opportunity_uuid="1",
        modified_fields=OpportunityUpdate(description="A new one"),
    )
    mock_client.execute_query.assert_called_once()


def test_delete_success(mock_client):
    mock_client.execute_query.return_value = None
    repository = OpportunityRepository(mock_client)
    repository.delete(opportunity_uuid="1")
    call_count = 1  # delete all edges to project
    call_count += 1  # delete opportunity vertex
    assert mock_client.execute_query.call_count == call_count
