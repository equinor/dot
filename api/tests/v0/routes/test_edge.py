from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from dependencies import create_app, create_versions
from src.v0.models.edge import EdgeResponse

from .. import database_version

app = create_app()
create_versions(app)
client = TestClient(app)


@pytest.fixture
def mock_service():
    with patch("src.v0.routes.edge.EdgeService") as MockService:
        yield MockService


def test_create_success(mock_service):
    mock_service.return_value.create.return_value = EdgeResponse(
        uuid="1", inV="2", outV="3", label="L", id="1"
    )
    edge_label = "L"
    response = client.post(
        f"/v{database_version}/edges/label/{edge_label}",
        params={
            "out_vertex_uuid": "2",
            "in_vertex_uuid": "4",
        },
    )
    assert response.status_code == 200
    mock_service.return_value.create.assert_called_once_with("2", "4", "L")


def test_read_all_edges_from_project_success(mock_service):
    mock_service.return_value.read_all_edges_from_project.return_value = [
        EdgeResponse(uuid="1", inV="2", outV="3", label="L", id="1")
    ]
    edge_label = "L"
    project_uuid = "2"
    response = client.get(
        f"/v{database_version}/projects/{project_uuid}/edges/label/{edge_label}"
    )
    assert response.status_code == 200
    mock_service.return_value.read_all_edges_from_project.assert_called_once_with(
        "2", "L"
    )


def test_read_all_edges_from_sub_project_success(mock_service):
    mock_service.return_value.read_all_edges_from_sub_project.return_value = [
        EdgeResponse(uuid="1", inV="2", outV="3", label="L", id="1")
    ]
    edge_label = "L"
    project_uuid = "2"
    vertex_uuid = ["5", "6", "7"]
    response = client.get(
        f"/v{database_version}/project/{project_uuid}/edges/label/{edge_label}/vertices/?vertex_uuid="
        + "&vertex_uuid=".join(vertex_uuid)
    )
    assert response.status_code == 200
    mock_service.return_value.read_all_edges_from_sub_project.assert_called_once_with(
        "2", "L", ["5", "6", "7"]
    )


def test_read_out_edge_from_vertex_success(mock_service):
    mock_service.return_value.read_out_edge_from_vertex.return_value = [
        EdgeResponse(uuid="1", inV="2", outV="3", label="L", id="1")
    ]
    edge_label = "L"
    vertex_uuid = "2"
    response = client.get(
        f"/v{database_version}/vertices/{vertex_uuid}/edges/label/{edge_label}/outgoing"
    )
    assert response.status_code == 200
    mock_service.return_value.read_out_edge_from_vertex.assert_called_once_with("2", "L")


def test_read_in_edge_to_vertex_success(mock_service):
    mock_service.return_value.read_in_edge_to_vertex.return_value = [
        EdgeResponse(uuid="1", inV="2", outV="3", label="L", id="1")
    ]
    edge_label = "L"
    vertex_uuid = "2"
    response = client.get(
        f"/v{database_version}/vertices/{vertex_uuid}/edges/label/{edge_label}/incoming"
    )
    assert response.status_code == 200
    mock_service.return_value.read_in_edge_to_vertex.assert_called_once_with("2", "L")


def test_read_success(mock_service):
    mock_service.return_value.read.return_value = EdgeResponse(
        uuid="1", inV="2", outV="3", label="L", id="1"
    )
    edge_id = "2"
    response = client.get(f"/v{database_version}/edges/{edge_id}")
    assert response.status_code == 200
    mock_service.return_value.read.assert_called_once_with("2")


# def test_update_success(mock_service):
#     mock_service.return_value.update.return_value = EdgeResponse(
#         uuid="1", inV="2", outV="3", label="L", id="1"
#     )
#     edge_id = "2"
#     edge_data = {"inV": "3"}
#     response = client.patch(f"/v{database_version}/edges/{edge_id}", json=edge_data)
#     assert response.status_code == 200
#     mock_service.return_value.update.assert_called_once_with("2", EdgeUpdate(inV="3"))


def test_delete_success(mock_service):
    mock_service.return_value.delete.return_value = None
    edge_id = "2"
    response = client.delete(f"/v{database_version}/edges/{edge_id}")
    assert response.status_code == 200
    mock_service.return_value.delete.assert_called_once_with("2")
