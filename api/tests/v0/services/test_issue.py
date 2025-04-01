from copy import deepcopy
from unittest.mock import MagicMock, patch

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
from src.v0.models.issue import IssueCreate, IssueResponse, IssueUpdate
from src.v0.models.meta import EdgeMetaDataResponse
from src.v0.repositories.issue import IssueRepository
from src.v0.services.issue import IssueService


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
def mock_edge_repository():
    with patch("src.v0.services.issue.EdgeRepository") as MockEdgeRepository:
        yield MockEdgeRepository


@pytest.fixture
def issue():
    data = {
        "shortname": "issue",
        "description": "an opportunity description",
        "tag": ["junk"],
        "category": "today",
        "uncertainty": 
            {
            "probability": {
                "dtype": "DiscreteUnconditionalProbability",
                "probability_function": [[0.3], [0.7]],
                "variables": {"variable": ["s1", "s2"]}
                },
            "key": "True",
            "source": "database analysis"
            },
        "decision": 
            {
                "states": ["yes", "no"],
                "decision_type": "Tactical"
            },
        "value_metric": None,
        "boundary": "in",
        "comments": [{"comment": "question","author": "John Doe"}],
        "index": "1234",
    }

    metadata = {
        "version": "v0",
        "uuid": "5",
        "timestamp": "1234",
        "date": "today",
        "id": "5",
        "label": "L",
        "ids": "ids",
    }

    return IssueResponse.model_validate(data | metadata)


def test_create_success(mock_client):
    mock_repository = MagicMock(spec=IssueRepository)
    service = IssueService(mock_client)
    service.repository = mock_repository

    service.create(
        project_uuid="1",
        issue_data=IssueCreate(description="A description", tag=["tag1", "tag2"]),
    )
    mock_repository.create.assert_called_once()


def test_read_issues_all_success(mock_client):
    mock_repository = MagicMock(spec=IssueRepository)
    service = IssueService(mock_client)
    service.repository = mock_repository

    service.read_issues_all(
        project_uuid="1",
        filter_model=Filter(),
    )
    mock_repository.read_issues_all.assert_called_once()


def test_read_success(mock_client):
    mock_repository = MagicMock(spec=IssueRepository)
    service = IssueService(mock_client)
    service.repository = mock_repository

    service.read(issue_uuid="1")
    mock_repository.read.assert_called_once()


def test_update_success(mock_client):
    mock_repository = MagicMock(spec=IssueRepository)
    service = IssueService(mock_client)
    service.repository = mock_repository

    service.update(issue_uuid="1", modified_fields=IssueUpdate(description="D"))
    mock_repository.update.assert_called_once()


def test_delete_success(mock_client):
    mock_repository = MagicMock(spec=IssueRepository)
    service = IssueService(mock_client)
    service.repository = mock_repository

    service.delete(issue_uuid="1")
    mock_repository.delete.assert_called_once()


def test_merge_src_merged_check_success(mock_client, mock_edge_repository, issue):
    src_issue = deepcopy(issue)
    src_issue.shortname = "src"
    src_issue.uuid = "1"

    dst_issue = deepcopy(issue)
    dst_issue.shortname = "dst"
    dst_issue.uuid = "2"

    merged_issue_data = deepcopy(issue)
    merged_issue_data.shortname = "dst"
    merged_issue_data.description = dst_issue.description
    merged_issue_data.uncertainty = {
        "probability": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.3], [0.7]],
            "variables": {"variable": ["s1", "s2"]}
            },
        "key": "True",
        "source": "database analysis"
        }
    merged_issue_data.comments = src_issue.comments + dst_issue.comments

    mock_repository = MagicMock(spec=IssueRepository)
    mock_repository._client = mock_client
    service = IssueService(mock_client)
    service.repository = mock_repository
    mock_edge_repository.return_value.read_in_edge_to_vertex.side_effect = [
        ["src"],
        [],
        [EdgeMetaDataResponse(uuid="123")],
    ]
    mock_repository.update.return_value = merged_issue_data

    service.merge(project_uuid="0", source_issue=src_issue, destination_issue=dst_issue)
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        "1", "merged_into"
    )
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        "2", "merged_into"
    )
    mock_repository.update.assert_called_once_with(
        src_issue.uuid,
        IssueCreate.model_validate(
            {
                k: v
                for k, v in merged_issue_data.model_dump().items()
                if k
                not in ["version", "uuid", "timestamp", "date", "id", "label", "ids"]
            }
        ),
    )
    mock_edge_repository.return_value.create.assert_any_call(
        out_vertex_uuid="2", in_vertex_uuid="5", edge_label="merged_into"
    )
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        vertex_uuid="2", edge_label="contains"
    )
    mock_edge_repository.return_value.delete.assert_called_once_with(edge_uuid="123")


def test_merge_dst_merged_check_success(mock_client, mock_edge_repository, issue):
    src_issue = deepcopy(issue)
    src_issue.shortname = "src"
    src_issue.uuid = "1"

    dst_issue = deepcopy(issue)
    dst_issue.shortname = "dst"
    dst_issue.uuid = "2"

    merged_issue_data = deepcopy(issue)
    merged_issue_data.shortname = "dst"
    merged_issue_data.description = dst_issue.description
    merged_issue_data.uncertainty = {
        "probability": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.3], [0.7]],
            "variables": {"variable": ["s1", "s2"]}
            },
        "key": "True",
        "source": "database analysis"
        }
    merged_issue_data.comments = src_issue.comments + dst_issue.comments

    mock_repository = MagicMock(spec=IssueRepository)
    mock_repository._client = mock_client
    service = IssueService(mock_client)
    service.repository = mock_repository
    mock_edge_repository.return_value.read_in_edge_to_vertex.side_effect = [
        [],
        ["dst"],
        [EdgeMetaDataResponse(uuid="123")],
    ]
    mock_repository.update.return_value = merged_issue_data

    service.merge(project_uuid="0", source_issue=src_issue, destination_issue=dst_issue)
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        "1", "merged_into"
    )
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        "2", "merged_into"
    )
    mock_repository.update.assert_called_once_with(
        dst_issue.uuid,
        IssueCreate.model_validate(
            {
                k: v
                for k, v in merged_issue_data.model_dump().items()
                if k
                not in ["version", "uuid", "timestamp", "date", "id", "label", "ids"]
            }
        ),
    )
    mock_edge_repository.return_value.create.assert_any_call(
        out_vertex_uuid="1", in_vertex_uuid="5", edge_label="merged_into"
    )
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        vertex_uuid="1", edge_label="contains"
    )
    mock_edge_repository.return_value.delete.assert_called_once_with(edge_uuid="123")


def test_merge_no_src_no_dst_merged_check_success(
    mock_client, mock_edge_repository, issue
):
    src_issue = deepcopy(issue)
    src_issue.shortname = "src"
    src_issue.uuid = "1"

    dst_issue = deepcopy(issue)
    dst_issue.shortname = "dst"
    dst_issue.uuid = "2"

    merged_issue_data = deepcopy(issue)
    merged_issue_data.shortname = "dst"
    merged_issue_data.description = dst_issue.description
    merged_issue_data.uncertainty = {
        "probability": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.3], [0.7]],
            "variables": {"variable": ["s1", "s2"]}
            },
        "key": "True",
        "source": "database analysis"
        }
    merged_issue_data.comments = src_issue.comments + dst_issue.comments

    mock_repository = MagicMock(spec=IssueRepository)
    mock_repository._client = mock_client
    service = IssueService(mock_client)
    service.repository = mock_repository
    mock_edge_repository.return_value.read_in_edge_to_vertex.side_effect = [
        [],
        [],
        [EdgeMetaDataResponse(uuid="123")],
        [EdgeMetaDataResponse(uuid="124")],
    ]
    mock_repository.create.return_value = merged_issue_data

    service.merge(project_uuid="0", source_issue=src_issue, destination_issue=dst_issue)
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        "1", "merged_into"
    )
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        "2", "merged_into"
    )
    mock_repository.create.assert_called_once_with(
        project_uuid="0",
        issue_data=IssueCreate.model_validate(
            {
                k: v
                for k, v in merged_issue_data.model_dump().items()
                if k
                not in ["version", "uuid", "timestamp", "date", "id", "label", "ids"]
            }
        ),
    )
    mock_edge_repository.return_value.create.assert_any_call(
        out_vertex_uuid="1", in_vertex_uuid="5", edge_label="merged_into"
    )
    mock_edge_repository.return_value.create.assert_any_call(
        out_vertex_uuid="2", in_vertex_uuid="5", edge_label="merged_into"
    )
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        vertex_uuid="1", edge_label="contains"
    )
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_any_call(
        vertex_uuid="2", edge_label="contains"
    )
    mock_edge_repository.return_value.delete.assert_any_call(edge_uuid="123")
    mock_edge_repository.return_value.delete.assert_any_call(edge_uuid="124")


def test_unmerge_success(mock_client, mock_edge_repository):
    mock_repository = MagicMock(spec=IssueRepository)
    mock_repository._client = mock_client
    service = IssueService(mock_client)
    service.repository = mock_repository
    mock_edge_repository.return_value.read_in_edge_to_vertex.return_value = [
        MagicMock(outV="1"),
        MagicMock(outV="2"),
    ]

    service.un_merge(project_uuid="0", merged_issue_uuid="1")
    mock_edge_repository.return_value.read_in_edge_to_vertex.assert_called_once_with(
        "1", "merged_into"
    )
    mock_edge_repository.return_value.create.assert_any_call(
        out_vertex_uuid="0", in_vertex_uuid="1", edge_label="contains"
    )
    mock_edge_repository.return_value.create.assert_any_call(
        out_vertex_uuid="0", in_vertex_uuid="2", edge_label="contains"
    )
    mock_repository.delete.assert_called_once_with("1")
