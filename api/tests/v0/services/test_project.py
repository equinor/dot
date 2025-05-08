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
from src.v0.models.project import ProjectCreate, ProjectUpdate
from src.v0.repositories.project import ProjectRepository
from src.v0.services.project import ProjectService


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
    mock_repository = MagicMock(spec=ProjectRepository)
    service = ProjectService(mock_client)
    service.repository = mock_repository

    service.create(
        project_data=ProjectCreate(name="A description"),
    )
    mock_repository.create.assert_called_once()


def test_read_projects_all_success(mock_client):
    mock_repository = MagicMock(spec=ProjectRepository)
    service = ProjectService(mock_client)
    service.repository = mock_repository

    service.read_projects_all()
    mock_repository.all.assert_called_once()


def test_read_success(mock_client):
    mock_repository = MagicMock(spec=ProjectRepository)
    service = ProjectService(mock_client)
    service.repository = mock_repository

    service.read(project_uuid="1")
    mock_repository.read.assert_called_once()


def test_export_project_success(mock_client):
    mock_repository = MagicMock(spec=ProjectRepository)
    service = ProjectService(mock_client)
    service.repository = mock_repository

    service.export_project(project_uuid="1")
    mock_repository.export_project.assert_called_once()


def test_import_project_success(mock_client):
    mock_repository = MagicMock(spec=ProjectRepository)
    service = ProjectService(mock_client)
    service.repository = mock_repository

    service.import_project(project_json={})
    mock_repository.import_project.assert_called_once()


def test_delete_success(mock_client):
    mock_repository = MagicMock(spec=ProjectRepository)
    service = ProjectService(mock_client)
    service.repository = mock_repository

    service.delete(project_uuid="1")
    mock_repository.delete.assert_called_once()


def test_update_success(mock_client):
    mock_repository = MagicMock(spec=ProjectRepository)
    service = ProjectService(mock_client)
    service.repository = mock_repository

    service.update(project_uuid="1", modified_fields=ProjectUpdate(name="New"))
    mock_repository.update.assert_called_once()


@patch("src.v0.services.project.generate_report")
def test_report_project_success(mock_report, mock_client):
    mock_repository = MagicMock(spec=ProjectRepository)
    mock_repository._client = mock_client
    service = ProjectService(mock_client)
    service.repository = mock_repository
    mock_repository.report_project.return_value = None

    service.report_project(project_uuid="1")
    mock_repository.report_project.assert_called_once()
    mock_report.assert_called_once_with(None, 1, "-", None)
