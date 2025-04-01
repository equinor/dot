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
from src.v0.models.filter import Filter
from src.v0.models.issue import IssueCreate, IssueUpdate
from src.v0.repositories.issue import IssueRepository


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
def issue():
    return {
        "shortname": ["issue"],
        "description": ["an opportunity description"],
        "tag": ['["junk"]'],
        "category": ["today"],
        "uncertainty": [(
            '{'
            '"probability": {'
                '"dtype": "DiscreteUnconditionalProbability",'
                '"probability_function": [[0.3], [0.7]],'
                '"variables": {"variable": ["s1", "s2"]}'
                '},'
            '"key": "True",'
            '"source": "database analysis"'
            '}'
        )],
        "decision": [(
            '{'
                '"states": ["yes", "no"],'
                '"decision_type": "Tactical"'
            '}'
        )],
        "value_metric": [None],
        "boundary": ["in"],
        "comments": [('[{"comment": "question","author": "John Doe"}]')],
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


def test_read_success(mock_client, issue, metadata):
    body = [{**issue, **metadata}]
    mock_client.execute_query.return_value = body
    repository = IssueRepository(mock_client)
    repository.read(issue_uuid="1")
    mock_client.execute_query.assert_called_once()


def test_read_issues_all_success(mock_client, issue, metadata):
    body = [{**issue, **metadata}]
    mock_client.execute_query.return_value = body
    repository = IssueRepository(mock_client)
    repository.read_issues_all(
        project_uuid="0", vertex_label="V", edge_label="L", filter_model=Filter()
    )
    mock_client.execute_query.assert_called_once()


def test_create_success(mock_client, issue, metadata):
    body_vertex = [{**issue, **metadata}]
    body_edge = ["e[x][1-L->2]"]
    mock_client.execute_query.side_effect = [body_vertex, body_edge]
    repository = IssueRepository(mock_client)
    repository.create(
        project_uuid="0",
        issue_data=IssueCreate.model_validate(
            {
                "description": "an issue description",
                "tag": ["junk"],
                "index": "1234",
                "category": "today",
            }
        ),
    )
    call_count = 1  # create issue vertex
    call_count += 1  # create edge to project
    assert mock_client.execute_query.call_count == call_count


def test_update_in_boundary_success(mock_client, issue, metadata):
    body = [{**issue, **metadata}]
    body[0]["description"] = ["A new one"]
    mock_client.execute_query.return_value = body
    repository = IssueRepository(mock_client)
    repository.update(
        issue_uuid="1",
        modified_fields=IssueUpdate(description="A new one"),
    )
    mock_client.execute_query.assert_called_once()


def test_update_out_boundary_success(mock_client, issue, metadata):
    body_vertex = [{**issue, **metadata}]
    body_vertex[0]["boundary"] = ["out"]
    body_vertex[0]["description"] = ["A new one"]
    body_vertex[0]["decision"] = [""]
    body_vertex[0]["uncertainty"] = [""]
    body_edge = ["e[x][1-L->2]"]
    mock_client.execute_query.side_effect = [
        body_vertex,
        body_edge,
        body_edge,
        None,
        None,
    ]
    repository = IssueRepository(mock_client)
    repository.update(
        issue_uuid="1",
        modified_fields=IssueUpdate(description="A new one", boundary="out"),
    )
    call_count = 1  # update issue vertex
    call_count += 1  # read edges from issue
    call_count += 1  # read edges to issue
    call_count += 1  # delete edges from issue
    call_count += 1  # delete edges to issue
    assert mock_client.execute_query.call_count == call_count


def test_delete_success(mock_client):
    mock_client.execute_query.return_value = None
    repository = IssueRepository(mock_client)
    repository.delete(issue_uuid="1")
    call_count = 1  # delete all edges to project
    call_count += 1  # delete objective vertex
    assert mock_client.execute_query.call_count == call_count
