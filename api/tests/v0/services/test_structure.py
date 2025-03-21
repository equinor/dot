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
from src.v0.models.edge import EdgeResponse
from src.v0.models.issue import IssueResponse
from src.v0.models.structure import InfluenceDiagramResponse
from src.v0.repositories.vertex import VertexRepository
from src.v0.services.structure import StructureService


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
    with patch("src.v0.services.structure.EdgeRepository") as MockEdgeRepository:
        yield MockEdgeRepository


@pytest.fixture
def graph():
    uncertainty = {
        "tag": ["Subsurface"],
        "category": "Uncertainty",
        "index": "0",
        "shortname": "Issue ABC",
        "description": "Bla",
        "keyUncertainty": "true",
        "decisionType": "",
        "alternatives": [""],
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.9, 0.1], [0.8, 0.2]],
            "variables": {"var1": ["out1", "out2"], "var2": ["in1", "in2"]},
        },
        "influenceNodeUUID": "",
        "boundary": "in",
        "comments": None,
        "uuid": "11-aa",
        "id": "11-aa",
    }

    decision = {
        "tag": ["Subsurface"],
        "category": "Decision",
        "index": "0",
        "shortname": "Issue ABC",
        "description": "Bla",
        "keyUncertainty": "",
        "decisionType": "Focus",
        "alternatives": ["yes", "no"],
        "probabilities": None,
        "influenceNodeUUID": "",
        "boundary": "in",
        "comments": None,
        "uuid": "22-bb",
        "id": "22-bb",
    }

    value_metric = {
        "tag": ["Subsurface"],
        "category": "Value Metric",
        "index": "0",
        "shortname": "Issue ABC",
        "description": "Bla",
        "keyUncertainty": "",
        "decisionType": "",
        "alternatives": [""],
        "probabilities": None,
        "influenceNodeUUID": "",
        "boundary": "in",
        "comments": None,
        "uuid": "33-cc",
        "id": "33-cc",
    }

    metadata = {
        "version": "v0",
        "timestamp": "1234",
        "date": "today",
        "id": "5",
        "label": "L",
        "ids": "ids",
    }
    data = [
        {**uncertainty, **metadata},
        {**decision, **metadata},
        {**value_metric, **metadata},
    ]

    return data


def test_read_influence_diagram_success(mock_client, mock_edge_repository, graph):
    vertices = [
        [IssueResponse.model_validate(graph[0])],
        [IssueResponse.model_validate(graph[1])],
        [IssueResponse.model_validate(graph[2])],
    ]
    edges = [
        EdgeResponse(
            uuid="101",
            id="101",
            outV="11-aa",
            inV="22-bb",
            label="influences",
        ),
        EdgeResponse(
            uuid="102",
            id="102",
            outV="22-bb",
            inV="33-cc",
            label="influences",
        ),
    ]

    mock_repository = MagicMock(spec=VertexRepository)
    mock_repository._client = mock_client
    service = StructureService(mock_client)
    service.repository = mock_repository
    mock_repository.read_out_vertex.side_effect = [
        vertices[0],
        [],
        vertices[1],
        [],
        vertices[2],
        [],
    ]
    mock_edge_repository.return_value.read_all_edges_from_sub_project.return_value = (
        edges
    )

    result = service.read_influence_diagram(project_uuid="0")
    assert isinstance(result, InfluenceDiagramResponse)


def test_create_decision_tree_success(mock_client, graph):
    vertices = [
        IssueResponse.model_validate(graph[0]),
        IssueResponse.model_validate(graph[1]),
        IssueResponse.model_validate(graph[2]),
    ]
    edges = [
        EdgeResponse(
            uuid="101",
            id="101",
            outV="11-aa",
            inV="22-bb",
            label="influences",
        ),
        EdgeResponse(
            uuid="102",
            id="102",
            outV="22-bb",
            inV="33-cc",
            label="influences",
        ),
    ]

    mock_repository = MagicMock(spec=VertexRepository)
    mock_repository._client = mock_client
    service = StructureService(mock_client)
    service.repository = mock_repository

    with patch(
        "src.v0.services.structure.StructureService.read_influence_diagram"
    ) as mocked_id:
        mocked_id.return_value = InfluenceDiagramResponse(vertices=vertices, edges=edges)
        result = service.create_decision_tree(project_uuid="0")

    assert result.children[0].children[0].children is None
    assert len(result.children[0].children) == 2
    assert len(result.children) == 4
    assert result.id.model_dump() == {
        "node_type": "UncertaintyNode",
        "shortname": "Issue ABC",
        "alternatives": None,
        "description": "Bla",
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.9, 0.1], [0.8, 0.2]],
            "variables": {"var1": ["out1", "out2"], "var2": ["in1", "in2"]},
        },
        "branch_name": "",
        "utility": None,
        "uuid": "11-aa",
    }
