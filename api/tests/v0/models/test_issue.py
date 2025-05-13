import pytest

from src.v0.models.issue import CommentData, IssueCreate, ProbabilityData


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
        "input_value={'comment': 'a comment'}, input_type=dict]\n" in str(exc.value)
    )


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
        "must be in ['DiscreteUnconditionalProbability', "
        "'DiscreteConditionalProbability']"
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
