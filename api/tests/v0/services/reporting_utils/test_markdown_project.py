import pytest

from src.v0.services.reporting_utils import markdown_project


@pytest.fixture
def project_data():
    return {
        "name": "the little project example",
        "description": "This is a project example",
        "tag": ["subsurface"],
        "decision_maker": "John Doe",
        "decision_date": "2021-01-01",
        "sensitivity_label": "Restricted",
        "index": "0",
    }


def test_project_description(project_data):
    assert markdown_project.project_description(project_data) == (
        "## Description\n\nThis is a project example \n\n"
    )


def test_project_information(project_data):
    assert markdown_project.project_information(project_data) == (
        "## Key information\n\n"
        "\n"
        "|||\n"
        "|:---|---:|\n"
        "| decision maker | John Doe |\n"
        "| decision date | 2021-01-01 |\n"
        "| sensitivity label | Restricted |\n"
        "\n"
        "\n"
    )


def test_generate_project_data(project_data):
    assert markdown_project.generate_project_data(project_data).startswith(
        "# Project: the little project example \n\n"
        "## Description\n\nThis is a project example \n"
    )


def test_generate_incomplete_project_data():
    project_data = {
        "version": "v0",
        "uuid": "72ba27a5-2e9c-4551-aa1a-6ad9d676d67b",
        "timestamp": "1742398642.7490323",
        "date": "2025-03-19 15:37:22.749036",
        "ids": "test",
        "name": "The Used Car Buyer Problem",
        "description": "The Used Car Buyer Problem",
        "tag": None,
        "decision_maker": "",
        "decision_date": "",
        "sensitivity_label": "Open",
        "index": "",
        "id": "72ba27a5-2e9c-4551-aa1a-6ad9d676d67b",
        "label": "project"
    }
    assert markdown_project.generate_project_data(project_data).startswith(
        "# Project: The Used Car Buyer Problem \n\n"
        "## Description\n\nThe Used Car Buyer Problem \n\n"
        "## Key information\n\n"
    )
