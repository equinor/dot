import numpy as np
import pytest

from src.v0.services.class_validations import validate_and_set_probability


def test_discrete_probability_variable_success_with_reformating():
    assert validate_and_set_probability.discrete_variables(
        {"v1": ["y", "n"], "v 2": ["r", "g", "b"]}
    ) == {
        "v1": ["y", "n"],
        "v_2": ["r", "g", "b"],
    }


def test_discrete_probability_variable_fail_not_dict(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_variables(None)
    assert [r.msg for r in caplog.records] == [
        (
            "One of the variables is not a dictionary with "
            "element being able to be interpreted as 1D: None"
        )
    ]
    assert str(exc_info.value) == (
        "One of the variables is not a dictionary with "
        "element being able to be interpreted as 1D: None"
    )


def test_discrete_probability_variable_fail_outcomes_not_as_list(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_variables({"v1": ["y", "n"], "v 2": 3})
    assert [r.msg for r in caplog.records] == [
        (
            "One of the variables is not a dictionary with "
            "element being able to be interpreted as 1D: {'v1': ['y', 'n'], 'v 2': 3}"
        )
    ]
    assert str(exc_info.value) == (
        "One of the variables is not a dictionary with "
        "element being able to be interpreted as 1D: {'v1': ['y', 'n'], 'v 2': 3}"
    )


def test_discrete_probability_variable_fail_not_as_array(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_variables(
            {"v1": ["y", "n"], "v 2": [["r", "g"], "b"]}
        )
    assert [r.msg for r in caplog.records] == [
        (
            "One of the variables is not a dictionary with "
            "element being able to be interpreted as 1D: "
            "setting an array element with a sequence. "
            "The requested array has an inhomogeneous shape "
            "after 1 dimensions. The detected shape was (2,) + inhomogeneous part."
        )
    ]
    assert str(exc_info.value) == (
        "One of the variables is not a dictionary with "
        "element being able to be interpreted as 1D: "
        "setting an array element with a sequence. "
        "The requested array has an inhomogeneous shape "
        "after 1 dimensions. The detected shape was (2,) + inhomogeneous part."
    )


def test_discrete_probability_variable_fail_not_as_1d(caplog):
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_variables(
            {"v1": ["y", "n"], "v 2": [["r", "g"], ["b", "a"]]}
        )
    assert [r.msg for r in caplog.records] == [
        (
            "One of the variables is not a dictionary with "
            "element being able to be interpreted as 1D: "
            "{'v1': ['y', 'n'], 'v 2': [['r', 'g'], ['b', 'a']]}"
        )
    ]
    assert str(exc_info.value) == (
        "One of the variables is not a dictionary with "
        "element being able to be interpreted as 1D: "
        "{'v1': ['y', 'n'], 'v 2': [['r', 'g'], ['b', 'a']]}"
    )


def test_discrete_conditional_probability_function_success_as_nan():
    conditioned_variable = {"v1": ["y", "n"]}
    conditioning_variable = {"v 2": ["r", "g", "b"]}
    pdf = np.full((2, 3), np.nan)
    result = validate_and_set_probability.discrete_conditional_probability_function(
        pdf, conditioned_variable, conditioning_variable
    )
    assert all(np.isnan(result).tolist())


def test_discrete_conditional_probability_function_success_as_normalized():
    conditioned_variable = {"v1": ["y", "n"]}
    conditioning_variable = {"v 2": ["r", "g", "b"]}
    pdf = np.array([[0.5, 1, 0], [0.5, 0, 1.0]])
    result = validate_and_set_probability.discrete_conditional_probability_function(
        pdf, conditioned_variable, conditioning_variable
    )
    np.testing.assert_allclose(pdf, result)


def test_discrete_conditional_probability_function_fail_not_array_like(caplog):
    conditioned_variable = {"v1": ["y", "n"]}
    conditioning_variable = {"v 2": ["r", "g", "b"]}
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_conditional_probability_function(
            None, conditioned_variable, conditioning_variable
        )
    assert [r.msg for r in caplog.records] == [
        (
            "The conditional probability function is not well "
            "formed size (not compatible with variables or "
            "content is not normalized): None"
        )
    ]
    assert str(exc_info.value) == (
        "The conditional probability function is not well "
        "formed size (not compatible with variables or "
        "content is not normalized): None"
    )


def test_discrete_conditional_probability_function_fail_not_normalized(caplog):
    conditioned_variable = {"v1": ["y", "n"]}
    conditioning_variable = {"v 2": ["r", "g", "b"]}
    pdf = np.array([[0.95, 1, 0], [0.5, 0, 1.0]])
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_conditional_probability_function(
            pdf, conditioned_variable, conditioning_variable
        )
    assert [r.msg for r in caplog.records] == [
        (
            "The conditional probability function is not well "
            "formed size (not compatible with variables or content is not normalized): "
            "[[0.95 1.   0.  ]\n [0.5  0.   1.  ]]"
        )
    ]
    assert str(exc_info.value) == (
        "The conditional probability function is not well "
        "formed size (not compatible with variables or content is not normalized): "
        "[[0.95 1.   0.  ]\n [0.5  0.   1.  ]]"
    )


def test_discrete_conditional_probability_function_fail_not_between_zero_and_one(caplog):
    conditioned_variable = {"v1": ["y", "n"]}
    conditioning_variable = {"v 2": ["r", "g", "b"]}
    pdf = np.array([[-1.5, 1, 0], [0.5, 0, 1.0]])
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_conditional_probability_function(
            pdf, conditioned_variable, conditioning_variable
        )
    assert [r.msg for r in caplog.records] == [
        (
            "The conditional probability function is not well "
            "formed size (not compatible with variables or content is not normalized): "
            "[[-1.5  1.   0. ]\n [ 0.5  0.   1. ]]"
        )
    ]
    assert str(exc_info.value) == (
        "The conditional probability function is not well "
        "formed size (not compatible with variables or content is not normalized): "
        "[[-1.5  1.   0. ]\n [ 0.5  0.   1. ]]"
    )


def test_discrete_conditional_probability_function_fail_not_consistent(caplog):
    conditioned_variable = {"v1": ["y", "n"]}
    conditioning_variable = {"v 2": ["r", "g", "b"]}
    pdf = np.array([[0, 1, 0], [0.5, 0, 0.5], [1, 0, 0]])
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_conditional_probability_function(
            pdf, conditioned_variable, conditioning_variable
        )
    assert [r.msg for r in caplog.records] == [
        (
            "The conditional probability function is not well "
            "formed size (not compatible with variables or content is not normalized): "
            "[[0.  1.  0. ]\n [0.5 0.  0.5]\n [1.  0.  0. ]]"
        )
    ]
    assert str(exc_info.value) == (
        "The conditional probability function is not well "
        "formed size (not compatible with variables or content is not normalized): "
        "[[0.  1.  0. ]\n [0.5 0.  0.5]\n [1.  0.  0. ]]"
    )


def test_discrete_unconditional_probability_function_success_as_None():
    variables = {"v1": ["y", "n"], "v 2": ["r", "g", "b"]}
    probability_function = [[None, None, None], [None, None, None]]
    pdf = np.array(probability_function)
    result = validate_and_set_probability.discrete_unconditional_probability_function(
        pdf, variables
    )
    assert all(np.isnan(result).tolist())


def test_discrete_unconditional_probability_function_success_as_nan():
    variables = {"v1": ["y", "n"], "v 2": ["r", "g", "b"]}
    pdf = np.full((2, 3), np.nan)
    result = validate_and_set_probability.discrete_unconditional_probability_function(
        pdf, variables
    )
    assert all(np.isnan(result).tolist())


def test_discrete_unconditional_probability_function_success_as_normalized():
    variables = {"v1": ["y", "n"], "v 2": ["r", "g", "b"]}
    pdf = np.array([[0, 0.25, 0], [0.25, 0, 0.5]])
    result = validate_and_set_probability.discrete_unconditional_probability_function(
        pdf, variables
    )
    np.testing.assert_allclose(pdf, result)


def test_discrete_unconditional_probability_function_fail_not_array_like(caplog):
    variables = {"v1": ["y", "n"], "v 2": ["r", "g", "b"]}
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_unconditional_probability_function(
            None, variables
        )
    assert [r.msg for r in caplog.records] == [
        (
            "The unconditional probability function is not well "
            "formed size (not compatible with variables or content "
            "is not normalized): None"
        )
    ]
    assert str(exc_info.value) == (
        "The unconditional probability function is not well "
        "formed size (not compatible with variables or content "
        "is not normalized): None"
    )


def test_discrete_unconditional_probability_function_fail_not_normalized(caplog):
    variables = {"v1": ["y", "n"], "v 2": ["r", "g", "b"]}
    pdf = np.array([[1, 1, 0], [0.5, 0, 0.5]])
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_unconditional_probability_function(
            pdf, variables
        )
    assert [r.msg for r in caplog.records] == [
        (
            "The unconditional probability function is not well formed "
            "size (not compatible with variables or content is not normalized): "
            "[[1.  1.  0. ]\n [0.5 0.  0.5]]"
        )
    ]
    assert str(exc_info.value) == (
        "The unconditional probability function is not well formed "
        "size (not compatible with variables or content is not normalized): "
        "[[1.  1.  0. ]\n [0.5 0.  0.5]]"
    )


def test_discrete_unconditional_probability_function_fail_not_between_zero_and_one(
    caplog,
):
    variables = {"v1": ["y", "n"], "v 2": ["r", "g", "b"]}
    pdf = np.array([[10, 1, 0], [0.5, 0, 0.5]])
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_unconditional_probability_function(
            pdf, variables
        )
    assert [r.msg for r in caplog.records] == [
        (
            "The unconditional probability function is not well "
            "formed size (not compatible with variables or content is not normalized): "
            "[[10.   1.   0. ]\n [ 0.5  0.   0.5]]"
        )
    ]
    assert str(exc_info.value) == (
        "The unconditional probability function is not well "
        "formed size (not compatible with variables or content is not normalized): "
        "[[10.   1.   0. ]\n [ 0.5  0.   0.5]]"
    )


def test_discrete_unconditional_probability_function_fail_not_consistent(caplog):
    variables = {"v1": ["y", "n"], "v 2": ["r", "g", "b"]}
    pdf = np.array([[0, 1, 0], [0.5, 0, 0.5], [1, 0, 0]])
    with pytest.raises(Exception) as exc_info:
        validate_and_set_probability.discrete_unconditional_probability_function(
            pdf, variables
        )
    assert [r.msg for r in caplog.records] == [
        (
            "The unconditional probability function is not well "
            "formed size (not compatible with variables or content is not normalized): "
            "[[0.  1.  0. ]\n [0.5 0.  0.5]\n [1.  0.  0. ]]"
        )
    ]
    assert str(exc_info.value) == (
        "The unconditional probability function is not well "
        "formed size (not compatible with variables or content is not normalized): "
        "[[0.  1.  0. ]\n [0.5 0.  0.5]\n [1.  0.  0. ]]"
    )
