import pytest

from src.v0.services.reporting_utils import markdown_opportunity


@pytest.fixture
def opportunity_data():
    return [
        {
            "description": "opportunistic opportunity",
            "tag": ["subsurface"],
            "index": "0",
            },
        {
            "description": "have fun",
            "tag": ["finance"],
            "index": "1",
            },
            ]


def test_generate_opportunity_data(opportunity_data):
    assert markdown_opportunity.generate_opportunity_data(opportunity_data) == (
            "## Opportunity statements\n\n"
            "  - opportunistic opportunity \n"
            "  - have fun \n"
            "\n"
            )