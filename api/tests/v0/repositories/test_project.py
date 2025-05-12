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
from src.v0.models.issue import IssueCreate
from src.v0.models.objective import ObjectiveCreate
from src.v0.models.opportunity import OpportunityCreate
from src.v0.models.project import ProjectCreate, ProjectUpdate
from src.v0.repositories.edge import EdgeRepository, EdgeResponse
from src.v0.repositories.issue import IssueRepository
from src.v0.repositories.objective import ObjectiveRepository
from src.v0.repositories.opportunity import OpportunityRepository
from src.v0.repositories.project import ProjectRepository


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
    mock_response.vertex = GremlinResponseBuilderVertex()
    mock_query.edge = GremlinStringQueryBuilderEdge()
    mock_response.edge = GremlinResponseBuilderEdge()

    # Set up the builder's query and response
    mock_builder.query = mock_query
    mock_builder.response = mock_response
    mock_client.builder = mock_builder

    return mock_client


@pytest.fixture
def project():
    return {
        "name": ["Project"],
        "tag": ['["tag1", "tag2"]'],
        "description": ["Description"],
        "index": ["0"],
        "decision_maker": ["Decision Maker"],
        "decision_date": ["2021-01-01"],
        "sensitivity_label": ["Restricted"],
    }


@pytest.fixture
def metadata():
    return {
        "version": ["v0"],
        "uuid": ["1"],
        "timestamp": ["2021-01-01"],
        "date": ["2021-01-01"],
        "T.id": "1",
        "T.label": "project",
    }


@pytest.fixture
def vertex():
    return {
        "T.id": "1",
        "T.label": "issue",
        "uuid": ["1"],
        "timestamp": ["2021-01-01"],
        "date": ["2021-01-01"],
        "version": ["v0"],
        "name": ["Project"],
        "tag": ['["tag1", "tag2"]'],
        "description": ["Description"],
        "type": ["Type"],
        "index": ["0"],
        "decision_maker": ["Decision Maker"],
        "decision_date": ["2021-01-01"],
        "sensitivity_label": ["Restricted"],
    }


@pytest.fixture
def edge():
    return "e[x][1-L->2]"


def test_read_success(mock_client, project, metadata):
    body = [{**project, **metadata}]
    mock_client.execute_query.return_value = body
    repository = ProjectRepository(mock_client)
    repository.read(project_uuid="1")
    mock_client.execute_query.assert_called_once()


def test_read_project_all_success(mock_client, project, metadata):
    body = [{**project, **metadata}]
    mock_client.execute_query.return_value = body
    repository = ProjectRepository(mock_client)
    repository.all()
    mock_client.execute_query.assert_called_once()


def test_create_success(mock_client, project, metadata):
    body = [{**project, **metadata}]
    mock_client.execute_query.return_value = body
    repository = ProjectRepository(mock_client)
    repository.create(
        project_data=ProjectCreate.model_validate(
            {
                "name": "Project",
                "tag": ["tag1", "tag2"],
                "description": "Description",
                "index": "0",
                "decision_maker": "Decision Maker",
                "decision_date": "2021-01-01",
                "sensitivity_label": "Restricted",
            }
        )
    )
    mock_client.execute_query.assert_called_once()


def test_update_success(mock_client, project, metadata):
    body = [{**project, **metadata}]
    mock_client.execute_query.return_value = body
    repository = ProjectRepository(mock_client)
    repository.update(
        project_uuid="1", modified_fields=ProjectUpdate(description="new Description")
    )
    mock_client.execute_query.assert_called_once()


def test_delete_success(mock_client, project, metadata, vertex):
    mock_client.execute_query.return_value = []
    mock_client.execute_query.side_effect = [[vertex], [], [], [], []]
    repository = ProjectRepository(mock_client)
    repository.delete(project_uuid="1")
    call_count = 1  # read vertex list
    call_count += 1  # read merged vertex
    call_count += 1  # read delete edge
    call_count += 1  # delete vertices
    call_count += 1  # delete project
    assert mock_client.execute_query.call_count == call_count


def test_filter_non_empty_fields(mock_client):
    # Create an instance of ProjectRepository
    project_repo = ProjectRepository(mock_client)

    # Test data
    data = {"a": "b", "c": "", "d": None, "e": "f"}
    exclude_keys = []

    # Expected result
    expected_result = {"a": "b", "e": "f"}

    # Call the _filter_non_empty_fields method
    result = project_repo._filter_non_empty_fields(data, exclude_keys)

    # Verify the result
    assert result == expected_result


def test_filter_non_empty_fields_exclude(mock_client):
    # Create an instance of ProjectRepository
    project_repo = ProjectRepository(mock_client)
    # Test data
    data = {"a": "b", "c": "", "d": "e"}
    exclude_keys = ["a"]

    # Expected result
    expected_result = {"d": "e"}

    # Call the _filter_non_empty_fields method
    result = project_repo._filter_non_empty_fields(data, exclude_keys)

    # Verify the result
    assert result == expected_result


def test_filter_list(mock_client):
    # Create an instance of ProjectRepository
    project_repo = ProjectRepository(mock_client)

    # Test data
    data = [{"a": "b", "c": "z"}, {"d": "e", "e": "x", "f": "g"}]
    exclude_keys = ["c"]

    # Expected result
    expected_result = [{"a": "b"}, {"d": "e", "e": "x", "f": "g"}]

    # Call the _filter_string method
    result = project_repo._filter_non_empty_fields(data, exclude_keys)

    # Verify the result
    assert result == expected_result


def test_filter_exclude_keys_none(mock_client):
    # Create an instance of ProjectRepository
    project_repo = ProjectRepository(mock_client)

    # Test data
    data = {"d": "e", "e": "x", "f": "g"}
    exclude_keys = None

    # Expected result
    expected_result = {"d": "e", "e": "x", "f": "g"}

    # Call the _filter_string method
    result = project_repo._filter_non_empty_fields(data, exclude_keys)

    # Verify the result
    assert result == expected_result


def test_filter_no_list_no_dict(mock_client):
    # Create an instance of ProjectRepository
    project_repo = ProjectRepository(mock_client)

    # Test data
    data = 5
    exclude_keys = ["a"]

    # Expected result
    expected_result = 5

    # Call the _filter_string method
    result = project_repo._filter_non_empty_fields(data, exclude_keys)

    # Verify the result
    assert result == expected_result


def test_export_project_success(mock_client, project, metadata, vertex, edge):
    body = [{**project, **metadata}]
    mock_client.execute_query.side_effect = [
        body,
        [vertex],
        [vertex],
        [vertex],
        [vertex],
        [edge],
        [edge],
        [edge],
        [edge],
    ]
    repository = ProjectRepository(mock_client)
    repository.export_project(project_uuid="1")
    call_count = 1  # read project
    call_count += 1  # read issue list
    call_count += 1  # read opportunity list
    call_count += 1  # read objective list
    call_count += 1  # read merged issues
    call_count += 1  # read contains edge list
    call_count += 1  # read influences edges
    call_count += 1  # read has_value_metric edges
    call_count += 1  # read merged edges
    assert mock_client.execute_query.call_count == call_count


def test_remove_contains_edge(mock_client):
    mock_client.execute_query.return_value = [
        {
            "id": "1",
            "outV": "2",
            "inV": "3",
            "label": "contains",
        }
    ]
    repository = ProjectRepository(mock_client)
    uuid = "1"

    with (
        patch.object(EdgeRepository, "read_in_edge_to_vertex") as mock_read,
        patch.object(EdgeRepository, "delete") as mock_delete,
    ):
        mock_read.return_value = [
            EdgeResponse(
                id="1",
                uuid="1",
                outV="2",
                inV="3",
                label="contains",
            )
        ]
        repository._remove_contains_edge(uuid)
        mock_read.assert_called_once_with(edge_label="contains", vertex_uuid=uuid)
        mock_delete.assert_called_once_with("1")


def test_create_project_components_vertices(mock_client):
    repository = ProjectRepository(mock_client)
    project_uuid = "1"
    project_json = {
        "vertices": {
            "issues": [
                {"id": "3", "label": "issue", "description": "Issue 1"},
            ],
            "opportunities": [
                {"id": "2", "label": "opportunity", "description": "Opportunity 1"}
            ],
            "objectives": [
                {"id": "5", "label": "objective", "description": "Objective 1"}
            ],
            "merged_issues": [
                {"id": "4", "label": "merged_issues", "description": "Merged Issue 1"}
            ],
        },
        "edges": [
            {"outV": "1", "inV": "2", "label": "contains"},
            {"outV": "2", "inV": "3", "label": "influences"},
        ],
    }

    with (
        patch.object(ObjectiveRepository, "create") as mock_create_objective,
        patch.object(OpportunityRepository, "create") as mock_create_opportunity,
        patch.object(IssueRepository, "create") as mock_create_issue,
        patch.object(
            ProjectRepository, "_remove_contains_edge"
        ) as mock_remove_contains_edge,
    ):
        mock_create_objective.return_value = MagicMock(uuid="new_uuid_5")
        mock_create_opportunity.return_value = MagicMock(uuid="new_uuid_2")
        mock_create_issue.side_effect = [
            MagicMock(uuid="new_uuid_3"),
            MagicMock(uuid="new_uuid_4"),
        ]

        for label, vertices in project_json["vertices"].items():
            repository._create_project_components_vertices(
                vertices, label, project_uuid, project_json
            )

        # Verify that the create methods were called with the correct arguments
        mock_create_objective.assert_called_once_with(
            project_uuid, ObjectiveCreate.model_validate({"description": "Objective 1"})
        )
        mock_create_opportunity.assert_called_once_with(
            project_uuid,
            OpportunityCreate.model_validate({"description": "Opportunity 1"}),
        )
        mock_create_issue.assert_any_call(
            project_uuid, IssueCreate.model_validate({"description": "Issue 1"})
        )
        mock_create_issue.assert_any_call(
            project_uuid, IssueCreate.model_validate({"description": "Merged Issue 1"})
        )

        # Verify that _remove_contains_edge was called for merged_issues
        mock_remove_contains_edge.assert_called_once_with("new_uuid_4")

        # Verify that the edges were updated correctly
        assert project_json["edges"][0]["outV"] == "1"
        assert project_json["edges"][0]["inV"] == "new_uuid_2"
        assert project_json["edges"][1]["outV"] == "new_uuid_2"
        assert project_json["edges"][1]["inV"] == "new_uuid_3"


def test_import_project(mock_client):
    repository = ProjectRepository(mock_client)
    project_json = {
        "vertices": {
            "project": {
                "name": "Project",
                "label": "project",
                "id": "1",
            },
            "issues": [
                {"id": "3", "label": "issue", "description": "Issue 1"},
            ],
            "opportunities": [
                {"id": "2", "label": "opportunity", "description": "Opportunity 1"}
            ],
            "objectives": [
                {"id": "5", "label": "objective", "description": "Objective 1"}
            ],
            "merged_issues": [
                {"id": "4", "label": "merged_issues", "description": "Merged Issue 1"}
            ],
        },
        "edges": [
            {"outV": "1", "inV": "2", "label": "contains"},
            {"outV": "2", "inV": "3", "label": "influences"},
        ],
    }
    with (
        patch.object(ProjectRepository, "create") as mock_create_project,
        patch.object(ObjectiveRepository, "create") as mock_create_objective,
        patch.object(OpportunityRepository, "create") as mock_create_opportunity,
        patch.object(IssueRepository, "create") as mock_create_issue,
        patch.object(
            ProjectRepository, "_remove_contains_edge"
        ) as mock_remove_contains_edge,
        patch.object(EdgeRepository, "create") as mock_create_edge,
    ):
        mock_create_project.return_value = MagicMock(uuid="new_uuid_1")
        mock_create_objective.return_value = MagicMock(uuid="new_uuid_5")
        mock_create_opportunity.return_value = MagicMock(uuid="new_uuid_2")
        mock_create_issue.side_effect = [
            MagicMock(uuid="new_uuid_3"),
            MagicMock(uuid="new_uuid_4"),
        ]

        repository.import_project(project_json)

        # Verify that the create methods were called with the correct arguments
        mock_create_project.assert_called_once_with(
            ProjectCreate.model_validate(
                {
                    "name": "Project",
                }
            )
        )
        mock_create_objective.assert_called_once_with(
            "new_uuid_1", ObjectiveCreate.model_validate({"description": "Objective 1"})
        )
        mock_create_opportunity.assert_called_once_with(
            "new_uuid_1",
            OpportunityCreate.model_validate({"description": "Opportunity 1"}),
        )
        mock_create_issue.assert_any_call(
            "new_uuid_1", IssueCreate.model_validate({"description": "Issue 1"})
        )
        mock_create_issue.assert_any_call(
            "new_uuid_1", IssueCreate.model_validate({"description": "Merged Issue 1"})
        )

        # Verify that _remove_contains_edge was called for merged_issues
        mock_remove_contains_edge.assert_called_once_with("new_uuid_4")

        # Verify that the edges were created correctly
        mock_create_edge.assert_any_call(
            edge_label="influences",
            out_vertex_uuid="new_uuid_2",
            in_vertex_uuid="new_uuid_3",
        )


def test_report_project_success(mock_client, project, metadata, vertex, edge):
    body = [{**project, **metadata}]
    mock_client.execute_query.side_effect = [
        body,
        [vertex],
        [vertex],
        [vertex],
        [vertex],
        [edge],
        [edge],
        [edge],
        [edge],
    ]
    repository = ProjectRepository(mock_client)
    repository.report_project(project_uuid="1")
    call_count = 1  # read project
    call_count += 1  # read issue list
    call_count += 1  # read opportunity list
    call_count += 1  # read objective list
    assert mock_client.execute_query.call_count == call_count
