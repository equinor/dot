from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from dependencies import create_app, create_versions
from src.v0.models.edge import EdgeResponse
from src.v0.models.issue import IssueResponse
from src.v0.models.structure import InfluenceDiagramResponse

from .. import database_version

app = create_app()
create_versions(app)
client = TestClient(app)


@pytest.fixture
def mock_service():
    with patch("src.v0.routes.structure.StructureService") as MockService:
        yield MockService


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
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
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
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
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
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
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


def test_read_influence_diagram_success(mock_service, graph):
    vertices = [
        IssueResponse.model_validate(graph[0]),
        IssueResponse.model_validate(graph[1]),
        IssueResponse.model_validate(graph[2]),
    ]
    edges = [
        EdgeResponse(
            uuid="101", id="101", outV="11-aa", inV="22-bb", label="influences"
        ),
        EdgeResponse(
            uuid="102", id="102", outV="22-bb", inV="33-cc", label="influences"
        ),
    ]
    mock_service.return_value.read_influence_diagram.return_value = (
        InfluenceDiagramResponse(vertices=vertices, edges=edges)
    )
    project_uuid = "0"
    response = client.get(
        f"/v{database_version}/projects/{project_uuid}/influence-diagram"
    )
    assert response.status_code == 200
    mock_service.return_value.read_influence_diagram.assert_called_once_with(
        project_uuid=project_uuid
    )


def test_convert_influence_diagram_to_decision_tree_model_success(mock_service, graph):
    mock_service.return_value.create_decision_tree.return_value = {
        "id": {
            "node_type": "UncertaintyNode",
            "shortname": "Issue ABC",
            "alternatives": None,
            "description": "Bla",
            "probabilities": None,
            "branch_name": "",
            "utility": None,
            "uuid": "11-aa",
        },
        "children": None,
    }
    project_uuid = "0"
    response = client.get(f"/v{database_version}/projects/{project_uuid}/decision-tree")
    assert response.status_code == 200
    mock_service.return_value.create_decision_tree.assert_called_once_with(
        project_uuid=project_uuid
    )
