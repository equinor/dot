from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from dependencies import create_versions, test_create_app
from src.v0.models.project import ProjectCreate, ProjectResponse, ProjectUpdate

from .. import database_version

app = test_create_app()
create_versions(app)
client = TestClient(app)


@pytest.fixture
def mock_service():
    with patch("src.v0.routes.project.ProjectService") as MockService:
        yield MockService


@pytest.fixture
def project():
    return {
        "name": "Project",
        "tag": ["tag1", "tag2"],
        "description": "Description",
        "index": "0",
        "decision_maker": "Decision Maker",
        "decision_date": "2021-01-01",
        "sensitivity_label": "Restricted",
    }


@pytest.fixture
def metadata():
    return {
        "version": "v0",
        "uuid": "1",
        "timestamp": "2021-01-01",
        "date": "2021-01-01",
        "T.id": "1",
        "T.label": "project",
    }


def test_create_success(mock_service, project, metadata):
    body = {**project, **metadata}
    mock_service.return_value.create.return_value = ProjectResponse.model_validate(body)
    response = client.post(f"/v{database_version}/projects", json=project)
    assert response.status_code == 200
    mock_service.return_value.create.assert_called_once_with(
        ProjectCreate.model_validate(project)
    )


def test_project_read_success(mock_service, project, metadata):
    body = {**project, **metadata}
    mock_service.return_value.read.return_value = ProjectResponse.model_validate(body)
    project_uuid = "1"
    response = client.get(f"/v{database_version}/projects/{project_uuid}")
    assert response.status_code == 200
    mock_service.return_value.read.assert_called_once_with(project_uuid)


def test_read_projects_all_success(mock_service, project, metadata):
    body = {**project, **metadata}
    mock_service.return_value.read_projects_all.return_value = [
        ProjectResponse.model_validate(body)
    ]
    response = client.get(f"/v{database_version}/projects")
    assert response.status_code == 200
    mock_service.return_value.read_projects_all.assert_called_once()


def test_delete_project_success(mock_service):
    project_uuid = "1"
    response = client.delete(f"/v{database_version}/projects/{project_uuid}")
    assert response.status_code == 200
    mock_service.return_value.delete.assert_called_once_with(project_uuid)


def test_update_project_success(mock_service, project, metadata):
    body = {**project, **metadata}
    body["name"] = "Updated Project"
    mock_service.return_value.update.return_value = ProjectResponse.model_validate(body)
    project_uuid = "1"
    response = client.patch(
        f"/v{database_version}/projects/{project_uuid}",
        json=ProjectUpdate(name="Updated Project").model_dump(),
    )
    assert response.status_code == 200
    mock_service.return_value.update.assert_called_once_with(
        project_uuid, ProjectUpdate(name="Updated Project")
    )


def test_import_project_success(mock_service, project, metadata):
    body = {
        "project": {**project, **metadata},
        "issues": [],
        "objectives": [],
        "opportunities": [],
        "edges": [],
    }
    mock_service.return_value.import_project.return_value = body
    response = client.post(f"/v{database_version}/projects/import", json=project)
    assert response.status_code == 200
    mock_service.return_value.import_project.assert_called_once_with(project)


def test_export_project_success(mock_service, project, metadata):
    body = {**project, **metadata}
    mock_service.return_value.export_project.return_value = body
    project_uuid = "1"
    response = client.get(f"/v{database_version}/projects/{project_uuid}/export")
    assert response.status_code == 200
    mock_service.return_value.export_project.assert_called_once_with(project_uuid)


def test_report_project_success(mock_service, project, metadata):
    body = {**project, **metadata}
    mock_service.return_value.report_project.return_value = body
    project_uuid = "1"
    response = client.get(
        f"/v{database_version}/projects/{project_uuid}/report",
        params={"level": 1, "filepath": "-"},
    )
    assert response.status_code == 200
    mock_service.return_value.report_project.assert_called_once_with(
        project_uuid, 1, "-"
    )
