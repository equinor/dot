import pytest

from src.v0.models.issue import (
    CommentData,
    DecisionData,
    IssueCreate,
    ProbabilityData,
    UncertaintyData,
)


def test_CommentData_success():
    assert CommentData(
        comment="a comment",
        author="an author",
    ).model_dump() == {
        "comment": "a comment",
        "author": "an author",
    }


def test_CommentData_fail():
    with pytest.raises(Exception) as exc:
        CommentData(
            comment="a comment",
        )
    assert (
        "1 validation error for CommentData\nauthor\n  Field required [type=missing, "
        "input_value={'comment': 'a comment'}, input_type=dict]\n    For further "
        "information visit https://errors.pydantic.dev/2.10/v/missing"
    ) in str(exc.value)


def test_ProbabilityData_default():
    assert ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        probability_function=[[0.4, 0.6]],
        variables={"var": ["state 1", "state 2"]},
    ).model_dump() == {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[0.4, 0.6]],
        "variables": {"var": ["state 1", "state 2"]},
    }


def test_ProbabilityData_fail():
    with pytest.raises(Exception) as exc:
        ProbabilityData(
            dtype="my_own_typ",
            probability_function=[[0.4, 0.6]],
            variables={"var": ["state 1", "state 2"]},
        )
    assert (
        "1 validation error for ProbabilityData\ndtype\n  "
        "Input should be 'DiscreteUnconditionalProbability' or 'DiscreteConditionalProbability' "
        "[type=literal_error, input_value='my_own_typ', input_type=str]\n    "
        "For further information visit https://errors.pydantic.dev/2.10/v/literal_error"
    ) in str(exc.value)


def test_ProbabilityData_update_states():
    pdf = ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        probability_function=[[None]],
        variables={"variable": ["outcome"]},
    )
    pdf.variables = {"variable": ["outcome", "state2"]}
    assert pdf.model_dump() == {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[None], [None]],
        "variables": {"variable": ["outcome", "state2"]},
    }
    pdf.variables = {"variable": ["outcome", "state2", "state3"]}
    assert pdf.model_dump() == {
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[None], [None], [None]],
        "variables": {"variable": ["outcome", "state2", "state3"]},
    }


def test_IssueData_default():
    issue = IssueCreate(description="a description")
    assert issue.model_dump() == {
        "tag": None,
        "category": None,
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
        "keyUncertainty": None,
        "decisionType": None,
        "alternatives": None,
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[None]],
            "variables": {"variable": ["outcome"]},
        },
        "influenceNodeUUID": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueData_update_states():
    issue = IssueCreate(description="a description")
    issue.probabilities.variables = {"variable": ["outcome", "state2"]}
    assert issue.model_dump() == {
        "tag": None,
        "category": None,
        "index": None,
        "shortname": None,
        "description": "a description",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
        "keyUncertainty": None,
        "decisionType": None,
        "alternatives": None,
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[None], [None]],
            "variables": {"variable": ["outcome", "state2"]},
        },
        "influenceNodeUUID": None,
        "boundary": None,
        "comments": None,
    }


def test_IssueData_probability_empty_shortname():
    issue = IssueCreate(description="a description", shortname="")
    assert issue.model_dump() == {
        "tag": None,
        "category": None,
        "index": None,
        "shortname": "",
        "description": "a description",
        "uncertainty": None,
        "decision": None,
        "value_metric": None,
        "keyUncertainty": None,
        "decisionType": None,
        "alternatives": None,
        "probabilities": {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [[None]],
            "variables": {"variable": ["outcome"]},
        },
        "influenceNodeUUID": None,
        "boundary": None,
        "comments": None,
    }


def test_UncertaintyData():
    uncertainty_data = UncertaintyData()
    assert uncertainty_data.probability is None
    assert uncertainty_data.key == "False"
    assert uncertainty_data.source == ""

    pdf = ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        probability_function=[[0.6], [0.4]],
        variables={"variable": ["s1", "s2"]},
    )
    uncertainty_data = UncertaintyData(
        probability=pdf, key="True", source="my own guess"
    )
    assert uncertainty_data.key == "True"
    assert uncertainty_data.source == "my own guess"


def test_DecisionData():
    decision_data = DecisionData()
    assert decision_data.states is None
    assert decision_data.decision_type is None

    decision_data = DecisionData(states=["yes", "no"], decision_type="Focus")
    assert decision_data.states == ["yes", "no"]
    assert decision_data.decision_type == "Focus"

    with pytest.raises(Exception) as exc:
        DecisionData(decision_type="not defined")
    assert (
        "1 validation error for DecisionData\ndecision_type\n  "
        "Input should be 'Focus', 'Tactical' or 'Strategic' "
        "[type=literal_error, input_value='not defined', input_type=str]\n    "
        "For further information visit https://errors.pydantic.dev/2.10/v/literal_error"
        ) in str(exc.value)
