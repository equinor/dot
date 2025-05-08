import pytest

from src.v0.services.reporting_utils import markdown_issue


@pytest.fixture
def fact_data():
    return [
        {
            "category": "Fact",
            "description": "Fact 1",
            "shortname": "F1",
            "boundary": "on",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Fact",
            "description": "Fact 2",
            "shortname": "F2",
            "boundary": "",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {},
        },
    ]


@pytest.fixture
def value_metric_data():
    return [
        {
            "category": "Value Metric",
            "description": "Value 1",
            "shortname": "V1",
            "boundary": "on",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Value Metric",
            "description": "Value 2",
            "shortname": "V2",
            "boundary": "out",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {},
        },
    ]


@pytest.fixture
def uncategorized_data():
    return [
        {
            "category": "",
            "description": "Nada 1",
            "shortname": "N1",
            "boundary": "",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "",
            "description": "Nada 2",
            "shortname": "N2",
            "boundary": "",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {},
        },
    ]


@pytest.fixture
def decision_data():
    return [
        {
            "category": "Decision",
            "description": "Decision 1",
            "shortname": "D1",
            "boundary": "on",
            "keyUncertainty": "",
            "decisionType": "Focus",
            "alternatives": ["yes", "no"],
            "probabilities": {},
        },
        {
            "category": "Decision",
            "description": "Decision 2",
            "shortname": "D2",
            "boundary": "out",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": ["yes", "no"],
            "probabilities": {},
        },
        {
            "category": "Decision",
            "description": "Decision 3",
            "shortname": "D3",
            "boundary": "in",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": ["yes", "no"],
            "probabilities": {},
        },
        {
            "category": "Decision",
            "description": "Decision 4",
            "shortname": "D4",
            "boundary": "in",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Decision",
            "description": "Decision 5",
            "shortname": "D5",
            "boundary": "in",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {},
        },
    ]


@pytest.fixture
def uncertainty_data():
    return [
        {
            "category": "Uncertainty",
            "description": "Uncertainty 1",
            "shortname": "U1",
            "boundary": "",
            "keyUncertainty": "",
            "decisionType": "None",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Uncertainty",
            "description": "Uncertainty 2",
            "shortname": "U2",
            "boundary": "in",
            "keyUncertainty": "true",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {
                "dtype": "DiscreteUnconditionalProbability",
                "probability_function": [[0.3], [0.7]],
                "variables": {"U2": ["low", "high"]},
            },
        },
        {
            "category": "Uncertainty",
            "description": "Uncertainty 3",
            "shortname": "U3",
            "boundary": "in",
            "keyUncertainty": "",
            "decisionType": "",
            "alternatives": [],
            "probabilities": {
                "dtype": "DiscreteUnconditionalProbability",
                "probability_function": [[0.6], [0.4]],
                "variables": {"U3": ["blue", "red"]},
            },
        },
    ]


@pytest.fixture
def issue_data(
    fact_data,
    value_metric_data,
    uncategorized_data,
    decision_data,
    uncertainty_data,
):
    return (
        fact_data
        + value_metric_data
        + uncategorized_data
        + decision_data
        + uncertainty_data
    )


def test_group_issues(issue_data):
    assert markdown_issue.group_issues(issue_data) == [
        {
            "category": "Fact",
            "description": "Fact 1",
            "shortname": "F1",
            "boundary": "on",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Fact",
            "description": "Fact 2",
            "shortname": "F2",
            "boundary": "Unset",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Decision",
            "description": "Decision 3",
            "shortname": "D3",
            "boundary": "in",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": ["yes", "no"],
            "probabilities": {},
        },
        {
            "category": "Decision",
            "description": "Decision 4",
            "shortname": "D4",
            "boundary": "in",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Decision",
            "description": "Decision 5",
            "shortname": "D5",
            "boundary": "in",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Decision",
            "description": "Decision 1",
            "shortname": "D1",
            "boundary": "on",
            "keyUncertainty": "Unset",
            "decisionType": "Focus",
            "alternatives": ["yes", "no"],
            "probabilities": {},
        },
        {
            "category": "Decision",
            "description": "Decision 2",
            "shortname": "D2",
            "boundary": "out",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": ["yes", "no"],
            "probabilities": {},
        },
        {
            "category": "Uncertainty",
            "description": "Uncertainty 2",
            "shortname": "U2",
            "boundary": "in",
            "keyUncertainty": "true",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {
                "dtype": "DiscreteUnconditionalProbability",
                "probability_function": [[0.3], [0.7]],
                "variables": {"U2": ["low", "high"]},
            },
        },
        {
            "category": "Uncertainty",
            "description": "Uncertainty 3",
            "shortname": "U3",
            "boundary": "in",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {
                "dtype": "DiscreteUnconditionalProbability",
                "probability_function": [[0.6], [0.4]],
                "variables": {"U3": ["blue", "red"]},
            },
        },
        {
            "category": "Uncertainty",
            "description": "Uncertainty 1",
            "shortname": "U1",
            "boundary": "Unset",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Value Metric",
            "description": "Value 1",
            "shortname": "V1",
            "boundary": "on",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Value Metric",
            "description": "Value 2",
            "shortname": "V2",
            "boundary": "out",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Uncategorized",
            "description": "Nada 1",
            "shortname": "N1",
            "boundary": "Unset",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {},
        },
        {
            "category": "Uncategorized",
            "description": "Nada 2",
            "shortname": "N2",
            "boundary": "Unset",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
            "alternatives": [],
            "probabilities": {},
        },
    ]


def test_clean_issues_facts(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.clean_issues(
        grouped, "Fact", ["description", "shortname", "boundary"]
    ) == [
        {"description": "Fact 1", "shortname": "F1", "boundary": "on"},
        {"description": "Fact 2", "shortname": "F2"},
    ]


def test_clean_issues_uncategorized(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.clean_issues(
        grouped, "Uncategorized", ["description", "shortname", "boundary"]
    ) == [
        {"description": "Nada 1", "shortname": "N1"},
        {"description": "Nada 2", "shortname": "N2"},
    ]


def test_keyword_translation(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    cleaned = markdown_issue.clean_issues(
        grouped, "Fact", ["description", "shortname", "boundary"]
    )
    assert markdown_issue.keyword_translation(cleaned, {"shortname": "nickname"}) == [
        {"description": "Fact 1", "nickname": "F1", "boundary": "on"},
        {"description": "Fact 2", "nickname": "F2"},
    ]


def test_add_facts(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_facts(grouped) == (
        "### Facts\n\n"
        "  1. - description: Fact 1 \n"
        "     - boundary: on \n"
        "     - shortname: F1 \n"
        "  1. - description: Fact 2 \n"
        "     - shortname: F2 \n\n"
    )


def test_add_action_item():
    grouped = [
        {
            "category": "Action Item",
            "description": "Fact 1",
            "shortname": "F1",
            "boundary": "on",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
        },
        {
            "category": "Action Item",
            "description": "Fact 2",
            "shortname": "F2",
            "boundary": "Unset",
            "keyUncertainty": "Unset",
            "decisionType": "Unset",
        },
    ]
    assert markdown_issue.add_action_item(grouped) == (
        "### Action items\n\n"
        "  1. - description: Fact 1 \n"
        "     - boundary: on \n"
        "     - shortname: F1 \n"
        "  1. - description: Fact 2 \n"
        "     - shortname: F2 \n\n"
    )


def test_add_value_metric(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_value_metric(grouped) == (
        "### Value metrics\n\n"
        "  1. - description: Value 1 \n"
        "     - boundary: on \n"
        "     - shortname: V1 \n"
        "  1. - description: Value 2 \n"
        "     - boundary: out \n"
        "     - shortname: V2 \n\n"
    )


def test_add_uncategorized(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_uncategorized(grouped) == (
        "### Uncategorized\n\n"
        "  1. - description: Nada 1 \n"
        "     - shortname: N1 \n"
        "  1. - description: Nada 2 \n"
        "     - shortname: N2 \n\n"
    )


def test_add_decision(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_decision(grouped) == (
        "### Decisions\n\n"
        "  1. - description: Decision 3 \n"
        "     - boundary: in \n"
        "     - shortname: D3 \n"
        "     - alternatives: \n"
        "       - yes \n"
        "       - no \n"
        "  1. - description: Decision 4 \n"
        "     - boundary: in \n"
        "     - shortname: D4 \n"
        "  1. - description: Decision 5 \n"
        "     - boundary: in \n"
        "     - shortname: D5 \n"
        "  1. - description: Decision 1 \n"
        "     - boundary: on \n"
        "     - shortname: D1 \n"
        "     - decision type: Focus \n"
        "     - alternatives: \n"
        "       - yes \n"
        "       - no \n"
        "  1. - description: Decision 2 \n"
        "     - boundary: out \n"
        "     - shortname: D2 \n"
        "     - alternatives: \n"
        "       - yes \n"
        "       - no \n\n"
    )


def test_add_uncertainty(issue_data):
    grouped = markdown_issue.group_issues(issue_data)
    assert markdown_issue.add_uncertainty(grouped) == (
        "### Uncertainties\n\n"
        "  1. - description: Uncertainty 2 \n"
        "     - boundary: in \n"
        "     - shortname: U2 \n"
        "     - key uncertainty: true \n"
        "     - probabilities: \n"
        "       - dtype: DiscreteUnconditionalProbability \n"
        "       - probability_function: \n"
        "           - 0.3 \n"
        "           - 0.7 \n"
        "       - variables: \n"
        "         - U2: \n"
        "           - low \n"
        "           - high \n"
        "  1. - description: Uncertainty 3 \n"
        "     - boundary: in \n"
        "     - shortname: U3 \n"
        "     - probabilities: \n"
        "       - dtype: DiscreteUnconditionalProbability \n"
        "       - probability_function: \n"
        "           - 0.6 \n"
        "           - 0.4 \n"
        "       - variables: \n"
        "         - U3: \n"
        "           - blue \n"
        "           - red \n"
        "  1. - description: Uncertainty 1 \n"
        "     - shortname: U1 \n\n"
    )


def test_generate_issue_data(issue_data):
    assert markdown_issue.generate_issue_data(issue_data) == (
        "## List of issues\n\n"
        "### Value metrics\n\n"
        "  1. - description: Value 1 \n"
        "     - boundary: on \n"
        "     - shortname: V1 \n"
        "  1. - description: Value 2 \n"
        "     - boundary: out \n"
        "     - shortname: V2 \n\n"
        "### Decisions\n\n"
        "  1. - description: Decision 3 \n"
        "     - boundary: in \n"
        "     - shortname: D3 \n"
        "     - alternatives: \n"
        "       - yes \n"
        "       - no \n"
        "  1. - description: Decision 4 \n"
        "     - boundary: in \n"
        "     - shortname: D4 \n"
        "  1. - description: Decision 5 \n"
        "     - boundary: in \n"
        "     - shortname: D5 \n"
        "  1. - description: Decision 1 \n"
        "     - boundary: on \n"
        "     - shortname: D1 \n"
        "     - decision type: Focus \n"
        "     - alternatives: \n"
        "       - yes \n"
        "       - no \n"
        "  1. - description: Decision 2 \n"
        "     - boundary: out \n"
        "     - shortname: D2 \n"
        "     - alternatives: \n"
        "       - yes \n"
        "       - no \n\n"
        "### Uncertainties\n\n"
        "  1. - description: Uncertainty 2 \n"
        "     - boundary: in \n"
        "     - shortname: U2 \n"
        "     - key uncertainty: true \n"
        "     - probabilities: \n"
        "       - dtype: DiscreteUnconditionalProbability \n"
        "       - probability_function: \n"
        "           - 0.3 \n"
        "           - 0.7 \n"
        "       - variables: \n"
        "         - U2: \n"
        "           - low \n"
        "           - high \n"
        "  1. - description: Uncertainty 3 \n"
        "     - boundary: in \n"
        "     - shortname: U3 \n"
        "     - probabilities: \n"
        "       - dtype: DiscreteUnconditionalProbability \n"
        "       - probability_function: \n"
        "           - 0.6 \n"
        "           - 0.4 \n"
        "       - variables: \n"
        "         - U3: \n"
        "           - blue \n"
        "           - red \n"
        "  1. - description: Uncertainty 1 \n"
        "     - shortname: U1 \n\n"
        "### Facts\n\n"
        "  1. - description: Fact 1 \n"
        "     - boundary: on \n"
        "     - shortname: F1 \n"
        "  1. - description: Fact 2 \n"
        "     - shortname: F2 \n\n"
        "### Uncategorized\n\n"
        "  1. - description: Nada 1 \n"
        "     - shortname: N1 \n"
        "  1. - description: Nada 2 \n"
        "     - shortname: N2 \n\n"
    )
