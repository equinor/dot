import numpy as np
import pytest
import xarray as xr

from src.v0.services.classes.discrete_conditional_probability import (
    DiscreteConditionalProbability,
)


@pytest.fixture
def cpt_2d():
    values = np.array([[0.1, 0.7, 0.6], [0.9, 0.3, 0.4]])
    conditioned_variable = {"A": ["yes", "no"]}
    conditioning_variable = {"B": ["low", "mid", "high"]}
    return DiscreteConditionalProbability(
        probability_function=values,
        variables=conditioned_variable|conditioning_variable
        )


def test_class_categorical_conditional_probability(cpt_2d):
    assert isinstance(cpt_2d._cpt, xr.DataArray)
    np.testing.assert_equal(cpt_2d._cpt.sel(A="yes"), np.array([0.1, 0.7, 0.6]))
    np.testing.assert_equal(cpt_2d._cpt.sel(A="no"), np.array([0.9, 0.3, 0.4]))
    np.testing.assert_equal(cpt_2d._cpt.sel(A="yes").sel(B="mid"), np.array([0.7]))


def test_outcomes():
    values = np.random.random((2, 3*3))
    for k in range(9):
        values[:, k] = values[:, k]/np.sum(values[:, k])
    values = np.reshape(values, (2, 3, 3))
    conditioned_variables = {"A": ["yes", "no"]}
    conditioning_variable = {"B": ["R", "G", "B"], "C": ["low", "mid", "high"]}
    cpt = DiscreteConditionalProbability(
        probability_function=values,
        variables=conditioned_variables|conditioning_variable
        )
    assert cpt.outcomes == (
        ("yes", "no")
    )

def test_outcomes_1d(cpt_2d):
    assert cpt_2d.outcomes == ("yes", "no")


def test_variables(cpt_2d):
    assert cpt_2d.variables == ("A", "B")


def test_conditioned_variables(cpt_2d):
    assert cpt_2d.conditioned_variables == ("A",)


def test_conditioning_variables(cpt_2d):
    assert cpt_2d.conditioning_variables == ("B",)


def test_initialize_nan():
    conditioned_variable = {"a": np.array([1, 2, 3])}
    conditioning_variables = {"b": np.array([4, 5]), "c": ["yes", "no"]}
    result = DiscreteConditionalProbability.initialize_nan(
        conditioned_variable,
        conditioning_variables=conditioning_variables
        )
    assert result._cpt.shape == (3, 2, 2)
    assert np.all(np.isnan(result._cpt))


# def test_initialize_nan_fail():
#     conditioned_variable = {
#         "a": np.array([1, 2, 3]),
#         "b": np.array([[4, 5, 6], [7, 8, 9]]),
#         "c": ["yes", "no"]
#         }
#     with pytest.raises(Exception) as exc:
#         DiscreteConditionalProbability.initialize_nan(variables=conditioned_variable)
#     assert str(exc.value) == "One of the variables cannot be interpreted as 1D"


def test_initialize_uniform():
    conditioned_variable = {"a": np.array([1, 2])}
    conditioning_variables = {"b": np.array([4, 5, 3]), "c": ["yes", "no"]}
    result = DiscreteConditionalProbability.initialize_uniform(
        conditioned_variables=conditioned_variable,
        conditioning_variables=conditioning_variables
        )
    assert result._cpt.shape == (2, 3, 2)
    assert np.all(result._cpt == 0.5)


def test_get_distribution(cpt_2d):
    np.testing.assert_allclose(
        cpt_2d.get_distribution(A="yes"), np.array([0.1, 0.7, 0.6])
        )
    assert cpt_2d.get_distribution(A="no", B="mid") == 0.3
