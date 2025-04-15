from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from dependencies import create_versions, test_create_app
from src.v0.models.filter import Filter
from src.v0.models.objective import ObjectiveCreate, ObjectiveResponse, ObjectiveUpdate

from .. import database_version

app = test_create_app()
create_versions(app)
client = TestClient(app)


@pytest.fixture
def mock_service():
    with patch("src.v0.routes.objective.ObjectiveService") as MockService:
        yield MockService


@pytest.fixture
def objective():
    return {
        "description": "an objective description",
        "tag": ["junk"],
        "index": "1234",
        "hierarchy": "fundamental",
    }


@pytest.fixture
def metadata():
    return {
        "version": "v0",
        "uuid": "1",
        "timestamp": "1234",
        "date": "today",
        "T.id": "1",
        "T.label": "L",
    }


def test_create_success(mock_service, objective, metadata):
    body = {**objective, **metadata}
    mock_service.return_value.create.return_value = ObjectiveResponse.model_validate(
        body
    )
    project_uuid = "0"
    response = client.post(
        f"/v{database_version}/projects/{project_uuid}/objectives", json=objective
    )
    assert response.status_code == 200
    mock_service.return_value.create.assert_called_once_with(
        project_uuid=project_uuid,
        objective_data=ObjectiveCreate.model_validate(objective),
    )


def test_objectives_all_success(mock_service, objective, metadata):
    body = {**objective, **metadata}
    mock_service.return_value.read_objectives_all.return_value = [
        ObjectiveResponse.model_validate(body)
    ]
    project_uuid = "0"
    response = client.get(f"/v{database_version}/projects/{project_uuid}/objectives")
    assert response.status_code == 200
    mock_service.return_value.read_objectives_all.assert_called_once_with(
        project_uuid=project_uuid, filter_model=Filter()
    )


def test_objectives_read_success(mock_service, objective, metadata):
    body = {**objective, **metadata}
    mock_service.return_value.read.return_value = ObjectiveResponse.model_validate(body)
    objective_uuid = "1"
    response = client.get(f"/v{database_version}/objectives/{objective_uuid}")

    assert response.status_code == 200
    mock_service.return_value.read.assert_called_once_with(objective_uuid)


def test_objectives_update_success(mock_service, objective, metadata):
    body = {**objective, **metadata}
    body["tag"] = ["important"]
    mock_service.return_value.update.return_value = ObjectiveResponse.model_validate(
        body
    )
    objective_uuid = "1"
    response = client.patch(
        f"/v{database_version}/objectives/{objective_uuid}",
        json=ObjectiveUpdate(tag=["important"]).model_dump(),
    )

    assert response.status_code == 200
    mock_service.return_value.update.assert_called_once_with(
        objective_uuid, ObjectiveUpdate(tag=["important"])
    )


def test_objectives_delete_success(mock_service):
    mock_service.return_value.delete.return_value = None
    objective_uuid = "1"
    response = client.delete(f"/v{database_version}/objectives/{objective_uuid}")

    assert response.status_code == 200
    mock_service.return_value.delete.assert_called_once_with(objective_uuid)
