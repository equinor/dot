from unittest.mock import patch

import numpy as np
import pytest

from src.v0.services.probability_utils.mep import mep
from src.v0.services.probability_utils.mep.validate import parse_config


@pytest.fixture
def config():
    return parse_config(
        {
            "joint_distributions": [
                "P000",
                "P001",
                "P010",
                "P011",
                "P100",
                "P101",
                "P110",
                "P111",
            ],
            "assessments": {
                "P.01": 0.4643,
                "P.11": 0.2411,
                "P1.1": 0.3490,
                "P00.": 0.1988,
                "P01.": 0.2463,
                "P10.": 0.3017,
                "P11.": 0.2532,
            },
            "equality": [],
            "inequality": [
                "P000 <= P001",
                "P001 - P010 >= 0",
                "P011 - P010 >= 0",
                "np.mean(P) >= 0.01 ",
                "0.13 >= np.mean(P)",
            ],
            "conditioned_variables": [1, 2],
            "minimization": {
                "bounds": {
                    "P000": [0.015, 1.0],
                    "P001": [0.03, 1],
                    "P010": [0, 1],
                    "P011": [0, 1],
                    "P100": [0, 0.021],
                    "P101": [0, 1],
                    "P110": [0, 1],
                    "P111": [0, 1],
                },
                "initial_guess": {
                    "P000": 0.015,
                    "P001": 0.04,
                    "P010": 0.01,
                    "P011": 0.2,
                    "P100": 0.02,
                    "P101": 0.3,
                    "P110": 0.2,
                    "P111": 0.05,
                },
            },
        }
    )


def test_probabilities_per_assessment(config):
    target = {
        "P.01": {"distributions": ["P001", "P101"], "indices": [1, 5]},
        "P.11": {"distributions": ["P011", "P111"], "indices": [3, 7]},
        "P00.": {"distributions": ["P000", "P001"], "indices": [0, 1]},
        "P01.": {"distributions": ["P010", "P011"], "indices": [2, 3]},
        "P1.1": {"distributions": ["P101", "P111"], "indices": [5, 7]},
        "P10.": {"distributions": ["P100", "P101"], "indices": [4, 5]},
        "P11.": {"distributions": ["P110", "P111"], "indices": [6, 7]},
    }
    result = mep.probabilities_per_assessment(
        config.joint_distributions, config.assessments
    )
    assert result == target


def test_marginalization_constraints(config):
    marginalization_indices = mep.probabilities_per_assessment(
        config.joint_distributions, config.assessments
    )
    result = mep.marginalization_constraints(marginalization_indices, config.assessments)
    assert len(result) == 7
    assert all(list(item.keys()) == ["type", "fun"] for item in result)
    assert all(item["type"] == "eq" for item in result)
    assert all(callable(item["fun"]) for item in result)


def test_replace_p_with_x():
    assert mep.replace_p_with_x("A + P - B * (P / C) + D * P") == "A+x-B*(x/C)+D*P"
    assert mep.replace_p_with_x("No replacement for P here") == "NoreplacementforPhere"


def test_replace_pijk_with_x_indexed():
    assert (
        mep.replace_pijk_with_x_indexed(
            "AA is BB or AA in CC but not A, B or C", ["AA", "BB", "CC"]
        )
        == "x[0]isx[1]orx[0]inx[2]butnotA,BorC"
    )
    assert (
        mep.replace_pijk_with_x_indexed("Hello World", ["Hello", "World"]) == "x[0]x[1]"
    )


@pytest.mark.parametrize(
    "cstring, distributions, target",
    [
        (
            "P000 <= P001",
            ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
            "-(x[0]-(x[1]))",
        ),
        (
            "P001 - P010 >= 0",
            ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
            "x[1]-x[2]-(0)",
        ),
        (
            "P011 - P010 >= 0",
            ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
            "x[3]-x[2]-(0)",
        ),
        (
            "np.mean(P) >= 0.01",
            ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
            "np.mean(x)-(0.01)",
        ),
        (
            "0.13 >= np.mean(P)",
            ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
            "0.13-(np.mean(x))",
        ),
        (
            "P000 + P001/2. = 0.7",
            ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
            "x[0]+x[1]/2.-(0.7)",
        ),
    ],
)
def test_parse_constraint(cstring, distributions, target):
    assert mep._parse_constraint(cstring, distributions) == target


def test_equality_constraints():
    result = mep.equality_constraints(
        ["P000 + P001/2. = 0.7"],
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
    )
    assert len(result) == 1
    assert all(list(item.keys()) == ["type", "fun"] for item in result)
    assert all(item["type"] == "eq" for item in result)
    assert all(callable(item["fun"]) for item in result)


def test_inequality_constraints():
    result = mep.inequality_constraints(
        ["P000 <= P001", "P011 - P010 >= 0"],
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
    )
    assert len(result) == 2
    assert all(list(item.keys()) == ["type", "fun"] for item in result)
    assert all(item["type"] == "ineq" for item in result)
    assert all(callable(item["fun"]) for item in result)


def test_all_constraints(config):
    result = mep.all_constraints(config)
    assert len(result) == 12
    assert all(list(item.keys()) == ["type", "fun"] for item in result)
    assert all(callable(item["fun"]) for item in result)
    assert all(item["type"] == "eq" for item in result[:6])
    assert all(item["type"] == "ineq" for item in result[7:])


@patch("src.v0.services.probability_utils.mep.mep.minimize")
def test_estimate(mocker):
    mep.maximize_entropy(constraints=[""], P0=["P0"], bnds=[(0, 1.0)])
    mocker.assert_called_once()


def test_solve_joint_probability():
    # Example from
    #   Ali E. Abbas
    #   Entropy Methods for Joint Distributions in Decision Analysis
    #   IEEE TRANSACTIONS ON ENGINEERING MANAGEMENT, VOL. 53, NO. 1, FEBRUARY 2006
    config = parse_config(
        {
            "joint_distributions": [
                "P000",
                "P001",
                "P010",
                "P011",
                "P100",
                "P101",
                "P110",
                "P111",
            ],
            "assessments": {
                "P.01": 0.4643,
                "P.11": 0.2411,
                "P1.1": 0.3490,
                "P00.": 0.1988,
                "P01.": 0.2463,
                "P10.": 0.3017,
                "P11.": 0.2532,
            },
            "equality": [],
            "inequality": [],
            "conditioned_variables": [],
            "minimization": {"bounds": {}, "initial_guess": {}},
        }
    )
    target = [0.0051, 0.1937, 0.0835, 0.1627, 0.0311, 0.2706, 0.1749, 0.0783]
    result = mep.solve_joint_probability(config)
    assert isinstance(result, dict)
    assert list(result.keys()) == [
        "P000",
        "P001",
        "P010",
        "P011",
        "P100",
        "P101",
        "P110",
        "P111",
    ]
    np.testing.assert_allclose(
        np.asarray(list(result.values())), np.asarray(target), rtol=1e-2, atol=1e-4
    )


def test_solve_joint_probability_with_constraints(config):
    # just check the solver works when constraints are given
    assert isinstance(mep.solve_joint_probability(config), dict)


def test_get_marginal_distribution(config):
    target = ["P0..", "P1.."]
    result = mep.get_marginal_distribution(config)
    assert all(item in target for item in result)
    assert all(item in result for item in target)


def test_to_conditional_probability(config):
    target = {
        "P000": 0.0342,
        "P001": 0.4125,
        "P010": 0.1651,
        "P011": 0.3882,
        "P100": 0.0378,
        "P101": 0.5059,
        "P110": 0.3332,
        "P111": 0.1231,
    }
    x0 = mep.solve_joint_probability(config)
    result = mep.to_conditional_probability(config, x0)
    np.testing.assert_allclose(
        np.asarray(list(result.values())),
        np.asarray(list(target.values())),
        rtol=1e-2,
        atol=1e-4,
    )


@patch("src.v0.services.probability_utils.mep.mep.to_conditional_probability")
@patch("src.v0.services.probability_utils.mep.mep.solve_joint_probability")
def test_solve(mocker_joint, mocker_conditional, config):
    mep.solve(config)
    mocker_joint.assert_called_once_with(config)
    mocker_conditional.assert_called_once()


@patch("src.v0.services.probability_utils.mep.mep.solve")
def test_mep_success(mocker):
    config = {
        "joint_distributions": [
            "P000",
            "P001",
            "P010",
            "P011",
            "P100",
            "P101",
            "P110",
            "P111",
        ],
        "assessments": {
            "P.01": 0.4643,
            "P.11": 0.2411,
            "P1.1": 0.3490,
            "P00.": 0.1988,
            "P01.": 0.2463,
            "P10.": 0.3017,
            "P11.": 0.2532,
        },
        "equality": [],
        "inequality": [
            "P000 <= P001",
            "P001 - P010 >= 0",
            "P011 - P010 >= 0",
            "np.mean(P) >= 0.01 ",
            "0.13 >= np.mean(P)",
        ],
        "conditioned_variables": [1, 2],
        "minimization": {
            "bounds": {
                "P000": [0.015, 1.0],
                "P001": [0.03, 1],
                "P010": [0, 1],
                "P011": [0, 1],
                "P100": [0, 0.021],
                "P101": [0, 1],
                "P110": [0, 1],
                "P111": [0, 1],
            },
            "initial_guess": {
                "P000": 0.015,
                "P001": 0.04,
                "P010": 0.01,
                "P011": 0.2,
                "P100": 0.02,
                "P101": 0.3,
                "P110": 0.2,
                "P111": 0.05,
            },
        },
    }
    mep.mep(config)
    mocker.assert_called_once_with(parse_config(config))


def test_mep_fail():
    config = {
        "joint_distributions": [
            "P000",
            "P001",
            "P010",
            "P011",
            "P100",
            "P101",
            "P110",
            "P111",
        ],
    }
    with pytest.raises(Exception) as exc:
        mep.mep(config)
    assert isinstance(exc.value, ValueError)
