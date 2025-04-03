import numpy as np
import pytest
import xarray as xr

from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)


@pytest.fixture
def cpt_2d():
    values = np.array([[0.1, 0.3, 0.2], [0.2, 0.1, 0.1]])
    coords = {"A": ["yes", "no"], "B": ["low", "mid", "high"]}
    return DiscreteUnconditionalProbability(values, coords)


def test_class_categorical_conditional_probability(cpt_2d):
    assert isinstance(cpt_2d._cpt, xr.DataArray)
    np.testing.assert_equal(cpt_2d._cpt.sel(A="yes"), np.array([0.1, 0.3, 0.2]))
    np.testing.assert_equal(cpt_2d._cpt.sel(A="no"), np.array([0.2, 0.1, 0.1]))
    np.testing.assert_equal(cpt_2d._cpt.sel(A="yes").sel(B="mid"), np.array([0.3]))


def test_outcomes(cpt_2d):
    assert cpt_2d.outcomes == (
        ("yes", "low"),
        ("yes", "mid"),
        ("yes", "high"),
        ("no", "low"),
        ("no", "mid"),
        ("no", "high"),
    )


def test_outcomes_1d():
    values = np.array([0.1, 0.9])
    coords = {"A": ["yes", "no"]}
    probability = DiscreteUnconditionalProbability(values, coords)
    assert probability.outcomes == ("yes", "no")


def test_variables(cpt_2d):
    assert cpt_2d.variables == ("A", "B")


def test_initialize_nan():
    coords = {"a": np.array([1, 2, 3]), "b": np.array([4, 5]), "c": ["yes", "no"]}
    result = DiscreteUnconditionalProbability.initialize_nan(variables=coords)
    assert result._cpt.shape == (3, 2, 2)
    assert np.all(np.isnan(result._cpt))


# def test_initialize_nan_fail():
#     coords = {
#         "a": np.array([1, 2, 3]),
#         "b": np.array([[4, 5, 6], [7, 8, 9]]),
#         "c": ["yes", "no"]
#         }
#     with pytest.raises(Exception) as exc:
#         DiscreteUnconditionalProbability.initialize_nan(variables=coords)
#     assert str(exc.value) == "One of the variables cannot be interpreted as 1D."


def test_initialize_uniform():
    coords = {"a": np.array([1, 2, 3]), "b": np.array([4, 5]), "c": ["yes", "no"]}
    result = DiscreteUnconditionalProbability.initialize_uniform(variables=coords)
    assert result._cpt.shape == (3, 2, 2)
    assert np.all(np.linalg.norm(result._cpt - 1 / 12) < 1e-12)


def test_get_distribution(cpt_2d):
    np.testing.assert_allclose(
        cpt_2d.get_distribution(A="yes"),
        np.array([0.1, 0.3, 0.2])
        )
    assert cpt_2d.get_distribution(A="no", B="mid") == 0.1
