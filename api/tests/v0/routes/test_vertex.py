from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from dependencies import create_app, create_versions
from src.v0.models.filter import Filter
from src.v0.models.vertex import VertexCreate, VertexResponse, VertexUpdate

from .. import database_version

app = create_app()
create_versions(app)
client = TestClient(app)


# Use the repository layer as service layer as there is no Vertex service layer
@pytest.fixture
def mock_service():
    with patch("src.v0.routes.vertex.VertexRepository") as MockService:
        yield MockService


@pytest.fixture
def metadata():
    return {
        "version": "v0",
        "uuid": "1",
        "timestamp": "1234",
        "date": "today",
        "T.id": "1",
    }


def test_create_success(mock_service, metadata):
    body = {**{"field": "3", "T.label": "V"}, **metadata}
    mock_service.return_value.create.return_value = VertexResponse.model_validate(body)
    vertex_label = "L"
    vertex_data = {"field": "3"}
    response = client.post(
        f"/v{database_version}/vertices/label/{vertex_label}", json=vertex_data
    )
    assert response.status_code == 200
    mock_service.return_value.create.assert_called_once_with(
        vertex_label, VertexCreate.model_validate(vertex_data)
    )


def test_read_vertex_all_success(mock_service, metadata):
    body = {**{"field": "3", "T.label": "V"}, **metadata}
    mock_service.return_value.read_vertex_all.return_value = (
        VertexResponse.model_validate(body)
    )
    vertex_label = "L"
    response = client.get(f"/v{database_version}/vertices/label/{vertex_label}")
    assert response.status_code == 200
    mock_service.return_value.all.assert_called_once_with(vertex_label)


def test_read_success(mock_service, metadata):
    body = {**{"field": "3", "T.label": "V"}, **metadata}
    mock_service.return_value.read.return_value = VertexResponse.model_validate(body)
    vertex_uuid = "1"
    response = client.get(f"/v{database_version}/vertices/{vertex_uuid}")
    assert response.status_code == 200
    mock_service.return_value.read.assert_called_once_with(vertex_uuid)


def test_read_out_vertex_success(mock_service, metadata):
    body = {**{"field": "3", "T.label": "V"}, **metadata}
    mock_service.return_value.read_out_vertex.return_value = [
        VertexResponse.model_validate(body)
    ]
    vertex_uuid = "1"
    params = {"edge_label": "V", "tag": "3"}
    response = client.get(
        f"/v{database_version}/vertices/{vertex_uuid}/children", params=params
    )
    assert response.status_code == 200
    filter_model = Filter(tag="3")
    mock_service.return_value.read_out_vertex.assert_called_once_with(
        vertex_uuid="1",
        edge_label="V",
        original_vertex_label=None,
        filter_model=filter_model,
    )


def test_read_in_vertex_success(mock_service, metadata):
    body = {**{"field": "3", "T.label": "V"}, **metadata}
    mock_service.return_value.read_in_vertex.return_value = [
        VertexResponse.model_validate(body)
    ]
    vertex_uuid = "1"
    params = {"edge_label": "V", "tag": "3"}
    response = client.get(
        f"/v{database_version}/vertices/{vertex_uuid}/parents", params=params
    )
    assert response.status_code == 200
    filter_model = Filter(tag="3")
    mock_service.return_value.read_in_vertex.assert_called_once_with(
        vertex_uuid="1",
        edge_label="V",
        original_vertex_label=None,
        filter_model=filter_model,
    )


def test_update_success(mock_service, metadata):
    body = {**{"field": "junk", "T.label": "V"}, **metadata}
    mock_service.return_value.update.return_value = VertexResponse.model_validate(body)
    vertex_uuid = "1"
    response = client.patch(
        f"/v{database_version}/vertices/{vertex_uuid}", json={"field": "junk"}
    )
    assert response.status_code == 200
    mock_service.return_value.update.assert_called_once_with(
        "1", VertexUpdate(field="junk")
    )


def test_delete_success(mock_service):
    mock_service.return_value.delete.return_value = None
    vertex_uuid = "1"
    response = client.delete(f"/v{database_version}/vertices/{vertex_uuid}")
    assert response.status_code == 200
    mock_service.return_value.delete.assert_called_once_with("1")
