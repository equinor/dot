import numpy as np
import pytest
import xarray as xr

from src.v0.models.issue import ProbabilityData
from src.v0.services.structure_utils.probability.discrete_unconditional_probability import (  # noqa: E501
    DiscreteUnconditionalProbability,
)


@pytest.fixture
def cpt_1d():
    values = np.array([0.3, 0.5, 0.2])
    coords = {"A": ["yes", "no", "maybe"]}
    return DiscreteUnconditionalProbability(values, coords)


@pytest.fixture
def cpt_2d():
    values = np.array([[0.1, 0.3, 0.2], [0.2, 0.1, 0.1]])
    coords = {"A": ["yes", "no"], "B": ["low", "mid", "high"]}
    return DiscreteUnconditionalProbability(values, coords)


@pytest.fixture
def cpt_3d():
    values = np.array(
        [
            [[0.02, 0.05, 0.03], [0.05, 0.02, 0.03], [0.05, 0.25, 0.05]],
            [[0.03, 0.02, 0.05], [0.05, 0.1, 0.02], [0.03, 0.05, 0.1]],
        ]
    )
    coords = {
        "A": ["yes", "no"],
        "B": ["low", "mid", "high"],
        "C": ["red", "green", "blue"],
    }
    return DiscreteUnconditionalProbability(values, coords)


def test_class_discrete_conditional_probability(cpt_2d):
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


def test_variables(cpt_2d):
    assert cpt_2d.variables == ("A", "B")


def test_from_db():
    data = ProbabilityData(
        **{
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": [
                [0.0, 0.0, 1.0, 1.0],
                [1.0, 0.0, 0.0, 0.0],
                [0.0, 1.0, 0.0, 0.0],
            ],
            "variables": {
                "Test Result": ["no Test", "Peach", "Lemon"],
                "Test": ["yes", "no"],
                "State": ["Peach", "Lemon"],
            },
        }
    )
    result = DiscreteUnconditionalProbability.from_db_model(data)
    assert result._cpt.shape == (3, 2, 2)
    assert result.get_distribution(TestResult="Peach", Test="yes", State="Peach") == 1.0


def test_initialize_nan():
    coords = {
        "a": np.array([1, 2, 3]),
        "b": np.array([4, 5]),
        "c": ["yes", "no"],
    }
    result = DiscreteUnconditionalProbability.initialize_nan(variables=coords)
    assert result._cpt.shape == (3, 2, 2)
    assert np.all(np.isnan(result._cpt))


def test_initialize_nan_fail():
    coords = {
        "a": np.array([1, 2, 3]),
        "b": np.array([[4, 5, 6], [7, 8, 9]]),
        "c": ["yes", "no"],
    }
    with pytest.raises(Exception) as exc:
        DiscreteUnconditionalProbability.initialize_nan(variables=coords)
    assert str(exc.value) == "One of the variables cannot be interpreted as 1D"


def test_set_to_uniform(cpt_2d):
    cpt_2d.set_to_uniform()
    assert np.all(np.linalg.norm(cpt_2d._cpt - 1 / 6) < 1e-12)


def test_normalize():
    values = np.array([[0.15, 0.2], [0.1, 0.05]])
    coords = {"A": ["low", "high"], "B": ["yes", "no"]}
    result = DiscreteUnconditionalProbability(values, coords)
    result.normalize()
    np.testing.assert_allclose(result._cpt, np.array([[0.3, 0.4], [0.2, 0.1]]))


def test_isnormalized(cpt_2d):
    assert cpt_2d.isnormalized()


def test_from_json(cpt_2d):
    stream = """{
        "dtype": "DiscreteUnconditionalProbability",
        "probability_function": [[0.1, 0.3, 0.2], [0.2, 0.1, 0.1]],
        "variables": {
            "A": ["yes", "no"],
            "B": ["low", "mid", "high"]
            }
    }"""
    result = DiscreteUnconditionalProbability.from_json(stream)
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
        DiscreteUnconditionalProbability.from_json(stream)
    assert str(exc.value) == "Expected DiscreteUnconditionalProbability dtype, got Junk"


def test_to_json_1d(cpt_1d):
    assert cpt_1d.to_json() == (
        '{"dtype": "DiscreteUnconditionalProbability", '
        '"probability_function": [[0.3], [0.5], [0.2]], '
        '"variables": {"A": ["yes", "no", "maybe"]}}'
    )


def test_to_json_2d(cpt_2d):
    assert cpt_2d.to_json() == (
        '{"dtype": "DiscreteUnconditionalProbability", '
        '"probability_function": [[0.1, 0.3, 0.2], [0.2, 0.1, 0.1]], '
        '"variables": {"A": ["yes", "no"], "B": ["low", "mid", "high"]}}'
    )


def test_to_json_3d(cpt_3d):
    assert cpt_3d.to_json() == (
        '{"dtype": "DiscreteUnconditionalProbability", '
        '"probability_function": '
        "[[0.02, 0.05, 0.03, 0.05, 0.02, 0.03, 0.05, 0.25, 0.05], "
        "[0.03, 0.02, 0.05, 0.05, 0.1, 0.02, 0.03, 0.05, 0.1]], "
        '"variables": {"A": ["yes", "no"], '
        '"B": ["low", "mid", "high"], '
        '"C": ["red", "green", "blue"]}}'
    )


def test_get_distribution(cpt_2d):
    np.testing.assert_allclose(
        cpt_2d.get_distribution(A="yes"), np.array([0.1, 0.3, 0.2])
    )
    assert cpt_2d.get_distribution(A="no", B="mid") == 0.1


def test_add_na_outcomes(cpt_2d):
    with pytest.raises(NotImplementedError):
        cpt_2d.add_na_outcomes()


def test_to_pyagrum_1d(cpt_1d):
    result = cpt_1d.to_pyagrum()
    target = [
        ({}, [0.3, 0.5, 0.2]),
    ]
    assert result == target


def test_to_pyagrum_1d_failed(cpt_2d):
    with pytest.raises(Exception) as exc:
        cpt_2d.to_pyagrum()
    assert str(exc.value) == "pyAgrum only takes 1D variables in UncertaintyNode"


def test_to_pycid(cpt_2d):
    with pytest.raises(NotImplementedError):
        cpt_2d.to_pycid()
