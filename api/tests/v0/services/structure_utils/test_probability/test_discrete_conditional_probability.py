import numpy as np
import pytest
import xarray as xr

from src.v0.models.issue import ProbabilityData
from src.v0.services.structure_utils.probability.discrete_conditional_probability import (  # noqa: E501
    DiscreteConditionalProbability,
)


@pytest.fixture
def cpt_2d():
    values = np.array([[0.1, 0.7, 0.6], [0.9, 0.3, 0.4]])
    coords = {"A": ["yes", "no"], "B": ["low", "mid", "high"]}
    return DiscreteConditionalProbability(values, coords)


@pytest.fixture
def cpt_3d():
    data = ProbabilityData(
        **{
            "dtype": "DiscreteConditionalProbability",
            "probability_function": [
                [0.1, 0.05, 0.85, 0.46],
                [0.7, 0.35, 0.12, 0.26],
                [0.2, 0.60, 0.03, 0.28],
            ],
            "variables": {
                "Test Result": ["no Test", "Peach", "Lemon"],
                "Test": ["yes", "no"],
                "State": ["Peach", "Lemon"],
            },
        }
    )
    return DiscreteConditionalProbability.from_db_model(data)


def test_class_discrete_conditional_probability(cpt_2d):
    assert isinstance(cpt_2d._cpt, xr.DataArray)
    np.testing.assert_equal(cpt_2d._cpt.sel(A="yes"), np.array([0.1, 0.7, 0.6]))
    np.testing.assert_equal(cpt_2d._cpt.sel(A="no"), np.array([0.9, 0.3, 0.4]))
    np.testing.assert_equal(cpt_2d._cpt.sel(A="yes").sel(B="mid"), np.array([0.7]))


def test_outcomes(cpt_2d):
    assert cpt_2d.outcomes == ("yes", "no")


def test_variables(cpt_2d):
    assert cpt_2d.variables == ("A", "B")


def test_from_db():
    data = ProbabilityData(
        **{
            "dtype": "DiscreteConditionalProbability",
            "probability_function": [
                [0.1, 0.05, 0.85, 0.46],
                [0.7, 0.35, 0.12, 0.26],
                [0.2, 0.60, 0.03, 0.28],
            ],
            "variables": {
                "Test Result": ["no Test", "Peach", "Lemon"],
                "Test": ["yes", "no"],
                "State": ["Peach", "Lemon"],
            },
        }
    )
    result = DiscreteConditionalProbability.from_db_model(data)
    assert result._cpt.shape == (3, 2, 2)
    assert result.get_distribution(TestResult="Peach", Test="yes", State="Peach") == 0.7
    assert result.get_distribution(TestResult="Lemon", Test="yes", State="Peach") == 0.2
    assert result.get_distribution(TestResult="Lemon", Test="yes", State="Lemon") == 0.6
    assert result.get_distribution(TestResult="Lemon", Test="no", State="Peach") == 0.03
    assert result.get_distribution(TestResult="Lemon", Test="no", State="Lemon") == 0.28


def test_initialize_nan():
    coords = {
        "a": np.array([1, 2, 3]),
        "b": np.array([4, 5]),
        "c": ["yes", "no"],
    }
    result = DiscreteConditionalProbability.initialize_nan(variables=coords)
    assert result._cpt.shape == (3, 2, 2)
    assert np.all(np.isnan(result._cpt))


def test_initialize_nan_fail():
    coords = {
        "a": np.array([1, 2, 3]),
        "b": np.array([[4, 5, 6], [7, 8, 9]]),
        "c": ["yes", "no"],
    }
    with pytest.raises(Exception) as exc:
        DiscreteConditionalProbability.initialize_nan(variables=coords)
    assert str(exc.value) == "One of the variables cannot be interpreted as 1D"


def test_set_to_uniform(cpt_2d):
    cpt_2d.set_to_uniform()
    assert np.all(cpt_2d._cpt == 0.5)


def test_normalize():
    values = np.array([[0.2, 0.2], [0.8, 0.2], [0.6, 0.4]])
    coords = {"A": ["low", "mid", "high"], "B": ["yes", "no"]}
    result = DiscreteConditionalProbability(values, coords)
    result.normalize()
    np.testing.assert_equal(result._cpt, np.array([[0.5, 0.5], [0.8, 0.2], [0.6, 0.4]]))


def test_normalize_2by2():
    values = np.array([[0.2, 0.2], [0.7, 0.3]])
    coords = {"A": ["low", "high"], "B": ["yes", "no"]}
    result = DiscreteConditionalProbability(values, coords)
    result.normalize()
    np.testing.assert_equal(result._cpt, np.array([[0.5, 0.5], [0.7, 0.3]]))


def test_isnormalized(cpt_2d):
    assert cpt_2d.isnormalized()


def test_from_json(cpt_2d):
    stream = """{
        "dtype": "DiscreteConditionalProbability",
        "probability_function": [[0.1, 0.7, 0.6], [0.9, 0.3, 0.4]],
        "variables": {
            "A": ["yes", "no"],
            "B": ["low", "mid", "high"]
            }
    }"""
    result = DiscreteConditionalProbability.from_json(stream)
    xr.testing.assert_allclose(result._cpt, cpt_2d._cpt)


def test_from_json_fail(cpt_2d):
    stream = """{
        "dtype": "Junk",
        "probability_function": [[0.1, 0.7, 0.6], [0.9, 0.3, 0.4]],
        "variables": {
            "A": ["yes", "no"],
            "B": ["low", "mid", "high"]
            }
    }"""
    with pytest.raises(Exception) as exc:
        DiscreteConditionalProbability.from_json(stream)
    assert str(exc.value) == "Expected DiscreteConditionalProbability dtype, got Junk"


def test_to_json(cpt_2d):
    assert cpt_2d.to_json() == (
        '{"dtype": "DiscreteConditionalProbability", '
        '"probability_function": [[0.1, 0.7, 0.6], [0.9, 0.3, 0.4]], '
        '"variables": {"A": ["yes", "no"], "B": ["low", "mid", "high"]}}'
    )


def test_get_distribution(cpt_2d):
    np.testing.assert_allclose(
        cpt_2d.get_distribution(A="yes"), np.array([0.1, 0.7, 0.6])
    )
    assert cpt_2d.get_distribution(A="no", B="mid") == 0.3


def test_add_conditioning_variable(cpt_2d):
    with pytest.raises(NotImplementedError):
        cpt_2d.add_conditioning_variable(None)


def test_remove_conditioning_variable(cpt_2d):
    with pytest.raises(NotImplementedError):
        cpt_2d.remove_conditioning_variable(None)


def test_add_na_outcomes(cpt_2d):
    with pytest.raises(NotImplementedError):
        cpt_2d.add_na_outcomes()


def test_to_pyagrum_2d(cpt_2d):
    result = cpt_2d.to_pyagrum()
    target = [
        ({"B": 0}, [0.1, 0.9]),
        ({"B": 1}, [0.7, 0.3]),
        ({"B": 2}, [0.6, 0.4]),
    ]
    assert result == target


def test_to_pyagrum_3d(cpt_3d):
    result = cpt_3d.to_pyagrum()
    target = [
        ({"Test": 0, "State": 0}, [0.10, 0.70, 0.20]),
        ({"Test": 0, "State": 1}, [0.05, 0.35, 0.60]),
        ({"Test": 1, "State": 0}, [0.85, 0.12, 0.03]),
        ({"Test": 1, "State": 1}, [0.46, 0.26, 0.28]),
    ]
    assert result == target


def test_to_pycid(cpt_2d):
    with pytest.raises(NotImplementedError):
        cpt_2d.to_pycid()
