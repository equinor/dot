from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from dependencies import create_app, create_versions
from src.v0.models.filter import Filter
from src.v0.models.issue import IssueCreate, IssueResponse, IssueUpdate

from .. import database_version

app = create_app()
create_versions(app)
client = TestClient(app)


@pytest.fixture
def mock_service():
    with patch("src.v0.routes.issue.IssueService") as MockService:
        yield MockService


@pytest.fixture
def issue():
    return {
        "shortname": "issue",
        "description": "an opportunity description",
        "tag": ["junk"],
        "index": "1234",
        "category": "today",
        "keyUncertainty": "true",
        "decisionType": "Tactical",
        "alternatives": ["yes", "no"],
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[0.9, 0.1]],
            "variables": {"var": ["out1", "out2"]},
        },
        "influenceNodeUUID": "",
        "boundary": "in",
        "comments": [{"comment": "question", "author": "John Doe"}],
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


def test_create_success(mock_service, issue, metadata):
    body = {**issue, **metadata}
    mock_service.return_value.create.return_value = IssueResponse.model_validate(body)
    project_uuid = "0"
    response = client.post(
        f"/v{database_version}/projects/{project_uuid}/issues", json=issue
    )
    assert response.status_code == 200
    mock_service.return_value.create.assert_called_once_with(
        project_uuid=project_uuid,
        issue_data=IssueCreate.model_validate(issue),
    )


def test_read_issues_all_success(mock_service, issue, metadata):
    body = {**issue, **metadata}
    mock_service.return_value.read_issue_all.return_value = [
        IssueResponse.model_validate(body)
    ]
    project_uuid = "0"
    response = client.get(f"/v{database_version}/projects/{project_uuid}/issues")
    assert response.status_code == 200
    mock_service.return_value.read_issues_all.assert_called_once_with(
        project_uuid=project_uuid, filter_model=Filter()
    )


def test_issues_read_success(mock_service, issue, metadata):
    body = {**issue, **metadata}
    mock_service.return_value.read.return_value = IssueResponse.model_validate(body)
    issue_uuid = "1"
    response = client.get(f"/v{database_version}/issues/{issue_uuid}")

    assert response.status_code == 200
    mock_service.return_value.read.assert_called_once_with(issue_uuid)


def test_issues_update_success(mock_service, issue, metadata):
    body = {**issue, **metadata}
    body["tag"] = ["important"]
    mock_service.return_value.update.return_value = IssueResponse.model_validate(body)
    issue_uuid = "1"
    response = client.patch(
        f"/v{database_version}/issues/{issue_uuid}",
        json=IssueUpdate(tag=["important"]).model_dump(),
    )

    assert response.status_code == 200
    mock_service.return_value.update.assert_called_once_with(
        issue_uuid, IssueUpdate(tag=["important"])
    )


def test_issues_delete_success(mock_service):
    mock_service.return_value.delete.return_value = None
    issue_uuid = "1"
    response = client.delete(f"/v{database_version}/issues/{issue_uuid}")

    assert response.status_code == 200
    mock_service.return_value.delete.assert_called_once_with(issue_uuid)


def test_issues_merge_success(mock_service, issue, metadata):
    body = {**issue, **metadata}
    body["tag"] = ["important"]
    mock_service.return_value.merge.return_value = IssueResponse.model_validate(body)

    src_issue = body
    dst_issue = body
    project_uuid = "0"
    response = client.post(
        f"/v{database_version}/projects/{project_uuid}/merge",
        json={"source_issue": src_issue, "destination_issue": dst_issue},
    )

    assert response.status_code == 200
    mock_service.return_value.merge.assert_called_once_with(
        project_uuid=project_uuid,
        source_issue=IssueResponse.model_validate(src_issue),
        destination_issue=IssueResponse.model_validate(dst_issue),
    )


def test_issues_unmerge_success(mock_service, issue, metadata):
    body = {**issue, **metadata}
    body["tag"] = ["important"]
    mock_service.return_value.merge.return_value = ["1", "2"]

    project_uuid = "0"
    merged_issue_uuid = body["uuid"]
    response = client.post(
        f"/v{database_version}/projects/{project_uuid}/un-merge/issues/{merged_issue_uuid}"
    )

    assert response.status_code == 200
    mock_service.return_value.un_merge.assert_called_once_with(
        project_uuid=project_uuid, merged_issue_uuid=merged_issue_uuid
    )
