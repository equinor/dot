from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from dependencies import create_app, create_versions
from src.v0.models.filter import Filter
from src.v0.models.opportunity import (
    OpportunityCreate,
    OpportunityResponse,
    OpportunityUpdate,
)

from .. import database_version

app = create_app()
create_versions(app)
client = TestClient(app)


@pytest.fixture
def mock_service():
    with patch("src.v0.routes.opportunity.OpportunityService") as MockService:
        yield MockService


@pytest.fixture
def opportunity():
    return {
        "description": "an opportunity description",
        "tag": ["junk"],
        "index": "1234",
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


def test_create_success(mock_service, opportunity, metadata):
    body = {**opportunity, **metadata}
    mock_service.return_value.create.return_value = OpportunityResponse.model_validate(
        body
    )
    project_uuid = "0"
    response = client.post(
        f"/v{database_version}/projects/{project_uuid}/opportunities", json=opportunity
    )
    assert response.status_code == 200
    mock_service.return_value.create.assert_called_once_with(
        project_uuid=project_uuid,
        opportunity_data=OpportunityCreate.model_validate(opportunity),
    )


def test_opportunities_all_success(mock_service, opportunity, metadata):
    body = {**opportunity, **metadata}
    mock_service.return_value.read_opportunities_all.return_value = [
        OpportunityResponse.model_validate(body)
    ]
    project_uuid = "0"
    response = client.get(f"/v{database_version}/projects/{project_uuid}/opportunities")
    assert response.status_code == 200
    mock_service.return_value.read_opportunities_all.assert_called_once_with(
        project_uuid=project_uuid, filter_model=Filter()
    )


def test_opportunities_read_success(mock_service, opportunity, metadata):
    body = {**opportunity, **metadata}
    mock_service.return_value.read.return_value = OpportunityResponse.model_validate(
        body
    )
    opportunity_uuid = "1"
    response = client.get(f"/v{database_version}/opportunities/{opportunity_uuid}")

    assert response.status_code == 200
    mock_service.return_value.read.assert_called_once_with(opportunity_uuid)


def test_opportunities_update_success(mock_service, opportunity, metadata):
    body = {**opportunity, **metadata}
    body["tag"] = ["important"]
    mock_service.return_value.update.return_value = OpportunityResponse.model_validate(
        body
    )
    opportunity_uuid = "1"
    response = client.patch(
        f"/v{database_version}/opportunities/{opportunity_uuid}",
        json=OpportunityUpdate(tag=["important"]).model_dump(),
    )

    assert response.status_code == 200
    mock_service.return_value.update.assert_called_once_with(
        opportunity_uuid, OpportunityUpdate(tag=["important"])
    )


def test_opportunities_delete_success(mock_service):
    mock_service.return_value.delete.return_value = None
    opportunity_uuid = "1"
    response = client.delete(f"/v{database_version}/opportunities/{opportunity_uuid}")

    assert response.status_code == 200
    mock_service.return_value.delete.assert_called_once_with(opportunity_uuid)
