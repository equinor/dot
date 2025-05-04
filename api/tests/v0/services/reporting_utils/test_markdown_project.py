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
        "## Description\n\n" "This is a project example \n"
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
    )
