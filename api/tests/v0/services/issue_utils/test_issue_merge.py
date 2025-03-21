import numpy as np

from src.v0.models.issue import IssueCreate, ProbabilityData
from src.v0.services.issue_utils.issue_merge import (
    _list_merge,
    _merge_probability_dtype,
    _merge_probability_function,
    _merge_probability_variables,
    _probability_merge,
    issue_merge,
)


def test_probability_merge_same_probability_data():
    source_probability = ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        variables={"Node 1": ["Outcome 1", "Outcome 2"]},
        probability_function=[[0.4], [0.6]],
    )
    destination_probability = ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        variables={"Node 1": ["Outcome 1", "Outcome 2"]},
        probability_function=[[0.4], [0.6]],
    )

    expected_output = ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        variables={"Node 1": ["Outcome 1", "Outcome 2"]},
        probability_function=[[0], [0]],
    )

    result = _probability_merge(source_probability, destination_probability)

    assert result == expected_output


def test_probability_merge_similar_structure_different_dtype():
    source_probability = ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        variables={"Node 1": ["Outcome 1", "Outcome 2"]},
        probability_function=[[0.4, 0.6]],
    )
    destination_probability = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2"],
            "Node 2": ["Condition 1", "Condition 2", "Condition 3"],
        },
        probability_function=[[0.4, 0.2, 0.4], [0.3, 0.6, 0.1]],
    )

    expected_output = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2"],
            "Node 2": ["Condition 1", "Condition 2", "Condition 3"],
        },
        probability_function=[[0, 0, 0], [0, 0, 0]],
    )

    result = _probability_merge(source_probability, destination_probability)

    assert result == expected_output


def test_probability_merge_updated_outcome_list():
    source_probability = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2"],
            "Node 3": ["Condition 3.1", "Condition 3.2"],
        },
        probability_function=[[0.4, 0.6], [0.4, 0.6]],
    )
    destination_probability = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2", "Outcome 3"],
            "Node 2": ["Condition 1", "Condition 2", "Condition 3"],
        },
        probability_function=[
            [0.4, 0.4, 0.2],
            [0.3, 0.4, 0.3],
            [0.3, 0.4, 0.3],
        ],
    )

    expected_output = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2", "Outcome 3"],
            "Node 3": ["Condition 3.1", "Condition 3.2"],
            "Node 2": ["Condition 1", "Condition 2", "Condition 3"],
        },
        probability_function=[
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0],
        ],
    )

    result = _probability_merge(source_probability, destination_probability)

    assert result == expected_output


def test_merge_probability_dtype_source_conditional():
    source_dtype = "DiscreteConditionalProbability"
    destination_dtype = "DiscreteUnconditionalProbability"

    expected_output = "DiscreteConditionalProbability"

    result = _merge_probability_dtype(destination_dtype, source_dtype)

    assert result == expected_output


def test_merge_probability_dtype_destination_conditional():
    source_dtype = "DiscreteUnconditionalProbability"
    destination_dtype = "DiscreteConditionalProbability"

    expected_output = "DiscreteConditionalProbability"

    result = _merge_probability_dtype(destination_dtype, source_dtype)

    assert result == expected_output


def test_merge_probability_dtype_unconditional():
    source_dtype = "DiscreteUnconditionalProbability"
    destination_dtype = "DiscreteUnconditionalProbability"

    expected_output = "DiscreteUnconditionalProbability"

    result = _merge_probability_dtype(destination_dtype, source_dtype)

    assert result == expected_output


def test_merge_probability_variables():
    source_variables = {
        "Node 1": ["Outcome 1", "Outcome 2"],
        "Node 3": ["Condition 3.1", "Condition 3.2"],
    }
    destination_variables = {
        "Node 1": ["Outcome 1", "Outcome 2", "Outcome 3"],
        "Node 2": ["Condition 1", "Condition 2", "Condition 3"],
    }

    expected_output = {
        "Node 1": ["Outcome 1", "Outcome 2", "Outcome 3"],
        "Node 3": ["Condition 3.1", "Condition 3.2"],
        "Node 2": ["Condition 1", "Condition 2", "Condition 3"],
    }

    result = _merge_probability_variables(destination_variables, source_variables)

    assert result == expected_output


def test_merge_probability_function():
    merged_variables = {
        "key1": ["outcome1", "outcome2"],
        "key2": ["outcome3", "outcome4", "outcome5"],
    }

    expected_output = np.zeros((2, 3), dtype=float)

    result = _merge_probability_function(merged_variables)

    assert np.array_equal(result, expected_output)


def test_probability_merge_updated_condition_list():
    source_probability = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2"],
            "Node 3": ["Condition 3.1", "Condition 3.2"],
        },
        probability_function=[[0.4, 0.6], [0.4, 0.6]],
    )
    destination_probability = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2", "Outcome 3"],
            "Node 3": ["Condition 3.1", "Condition 3.2", "Condition 3.3"],
            "Node 2": ["Condition 1", "Condition 2", "Condition 3"],
        },
        probability_function=[
            [0.4, 0.4, 0.2],
            [0.3, 0.4, 0.3],
            [0.3, 0.4, 0.3],
        ],
    )

    expected_output = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2", "Outcome 3"],
            "Node 3": ["Condition 3.1", "Condition 3.2", "Condition 3.3"],
            "Node 2": ["Condition 1", "Condition 2", "Condition 3"],
        },
        probability_function=[
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
    )

    result = _probability_merge(destination_probability, source_probability)

    assert result == expected_output


def test_probability_merge_unconditional_not_identical_variables():
    source_probability = ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        variables={
            "Node 1": ["Outcome 1"],
        },
        probability_function=[[1]],
    )
    destination_probability = ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        variables={
            "Node 2": ["Outcome 1"],
        },
        probability_function=[[1]],
    )

    expected_output = ProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        variables={
            "Node 2": ["Outcome 1"],
        },
        probability_function=[[0.0]],
    )

    result = _probability_merge(destination_probability, source_probability)

    assert result == expected_output


def test_probability_merge_updated_no_src_dst():
    source_probability = None
    destination_probability = None

    expected_output = None
    result = _probability_merge(destination_probability, source_probability)

    assert result == expected_output


def test_probability_merge_updated_no_dst():
    source_probability = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2"],
            "Node 3": ["Condition 3.1", "Condition 3.2"],
        },
        probability_function=[[0.4, 0.6], [0.4, 0.6]],
    )
    destination_probability = None

    expected_output = source_probability
    result = _probability_merge(destination_probability, source_probability)

    assert result == expected_output


def test_probability_merge_updated_no_src():
    source_probability = None
    destination_probability = ProbabilityData(
        dtype="DiscreteConditionalProbability",
        variables={
            "Node 1": ["Outcome 1", "Outcome 2"],
            "Node 3": ["Condition 3.1", "Condition 3.2"],
        },
        probability_function=[[0.4, 0.6], [0.4, 0.6]],
    )

    expected_output = destination_probability
    result = _probability_merge(destination_probability, source_probability)

    assert result == expected_output


def test_merge_issue():
    source_issue = IssueCreate(
        tag=["Tagging tag"],
        category="Uncertainty",
        index="1",
        shortname="Source Issue",
        description="This is a description of the source issue",
        keyUncertainty=None,
        decisionType="Focus",
        alternatives=["Alternative A", "Alternative B"],
        probabilities=ProbabilityData(
            dtype="DiscreteConditionalProbability",
            variables={
                "Node 1": ["Outcome 1", "Outcome 2"],
                "Node 3": ["Condition 3.1", "Condition 3.2"],
            },
            probability_function=[[0.4, 0.6], [0.4, 0.6]],
        ),
        influenceNodeUUID=None,
        comments=[{"comment": "src comment", "author": "John Doe"}],
    )

    destination_issue = IssueCreate(
        tag=["Togging tog"],
        category="Decision",
        index="100",
        shortname="Destination Issue",
        description="This is a description of the destination issue",
        keyUncertainty=None,
        decisionType="Focus",
        alternatives=["Alternative C", "Alternative D"],
        probabilities=ProbabilityData(
            dtype="DiscreteConditionalProbability",
            variables={
                "Node 1": ["Outcome 1", "Outcome 2"],
                "Node 3": ["Condition 3.1", "Condition 3.2"],
            },
            probability_function=[[0.4, 0.6], [0.4, 0.6]],
        ),
        influenceNodeUUID=None,
        comments=[{"comment": "dst comment", "author": "John Doe 2"}],
    )
    expected_output = IssueCreate(
        tag=list({"Togging tog", "Tagging tag"}),
        category="Decision",
        index="100",
        shortname="Destination Issue",
        description=(
            "This is a description of the destination issue This is a "
            "description of the source issue"
        ),
        keyUncertainty=None,
        decisionType="Focus",
        alternatives=[
            "Alternative C",
            "Alternative D",
            "Alternative A",
            "Alternative B",
        ],
        probabilities=ProbabilityData(
            dtype="DiscreteConditionalProbability",
            variables={
                "Node 1": ["Outcome 1", "Outcome 2"],
                "Node 3": ["Condition 3.1", "Condition 3.2"],
            },
            probability_function=[[0, 0], [0, 0]],
        ),
        influenceNodeUUID="",
        comments=[
            {"comment": "dst comment", "author": "John Doe 2"},
            {"comment": "src comment", "author": "John Doe"},
        ],
    )

    result = issue_merge(source_issue, destination_issue)
    assert result == expected_output


def test__list_merge():
    assert _list_merge("", "") == ""
    assert _list_merge("", "[a string]") == "[a string]"
    assert _list_merge("[a string]", "") == "[a string]"
    assert (
        _list_merge("[1, 2, 3, 4, 5]", "['a', 'b', 'c', 'd']")
        == '[1, 2, 3, 4, 5, "a", "b", "c", "d"]'
    )
