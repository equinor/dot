import pytest

from src.v0.services.reporting_utils import markdown_objective


@pytest.fixture
def objective_data():
    return [
        {
            "description": "objectively objecting the objectives 1",
            "hierarchy": "Fundamental",
            "tag": ["subsurface"],
            "index": "0",
        },
        {
            "description": "objectively objecting the objectives 2",
            "hierarchy": "Mean",
            "tag": ["subsurface"],
            "index": "0",
        },
        {
            "description": "objectively objecting the objectives 3",
            "hierarchy": "",
            "tag": ["subsurface"],
            "index": "0",
        },
    ]


def test_group_objectives(objective_data):
    assert markdown_objective.group_objectives(objective_data) == {
        "Strategic": [],
        "Fundamental": [
            {
                "description": "objectively objecting the objectives 1",
                "hierarchy": "Fundamental",
                "tag": ["subsurface"],
                "index": "0",
            }
        ],
        "Mean": [
            {
                "description": "objectively objecting the objectives 2",
                "hierarchy": "Mean",
                "tag": ["subsurface"],
                "index": "0",
            }
        ],
        "Uncategorized": [
            {
                "description": "objectively objecting the objectives 3",
                "hierarchy": "",
                "tag": ["subsurface"],
                "index": "0",
            }
        ],
    }


def test_add_objectives(objective_data):
    grouped_data = markdown_objective.group_objectives(objective_data)
    assert markdown_objective.add_objectives(grouped_data, "Uncategorized") == (
        "### Uncategorized\n\n" "  - objectively objecting the objectives 3 \n\n"
    )


def test_generate_objective_data(objective_data):
    assert markdown_objective.generate_objective_data(objective_data) == (
        "## Objectives\n\n"
        "### Fundamental\n\n"
        "  - objectively objecting the objectives 1 \n\n"
        "### Mean\n\n"
        "  - objectively objecting the objectives 2 \n\n"
        "### Uncategorized\n\n"
        "  - objectively objecting the objectives 3 \n\n"
    )
