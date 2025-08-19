import json
from collections import namedtuple
from pathlib import Path
from unittest.mock import mock_open, patch

import pytest

from src.v0.services.probability_utils.mep import validate


@pytest.fixture
def config_conditional_probability():
    return {
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


def test_read_config():
    mock_json_data = json.dumps({"key1": "value1", "key2": "value2"})

    with patch("builtins.open", mock_open(read_data=mock_json_data)):
        config_file = Path("config.json")
        config = validate.read_config(config_file)

        assert config == {"key1": "value1", "key2": "value2"}


def test_parse_config(config_conditional_probability):
    assert isinstance(
        validate.parse_config(config_conditional_probability), validate.Configuration
    )


def test_parse_config_no_bound(config_conditional_probability):
    config_conditional_probability["minimization"]["bounds"] = []
    result = validate.parse_config(config_conditional_probability)
    assert list(result.minimization.bounds.keys()) == [
        "P000",
        "P001",
        "P010",
        "P011",
        "P100",
        "P101",
        "P110",
        "P111",
    ]
    assert list(result.minimization.bounds.values()) == [(0, 1.0)] * 8


def test_validate_input_dicitonary_success(config_conditional_probability):
    assert validate.validate_input_dictionary(config_conditional_probability)


def test_validate_input_dicitonary_fail_only_joint_distributions():
    assert not validate.validate_input_dictionary({"joint_distributions": ["P000"]})


def test_validate_input_dicitonary_fail_no_bounds():
    config = {
        "joint_distributions": ["P000"],
        "assessments": {"P.01": 0.4643},
        "equality": [],
        "inequality": [],
        "conditioned_variables": [],
        "minimization": {
            "initial_guess": {
                "P000": 0.015,
            }
        },
    }
    assert not validate.validate_input_dictionary(config)


def test_parse_config_no_initial_guess(config_conditional_probability):
    config_conditional_probability["minimization"]["initial_guess"] = []
    result = validate.parse_config(config_conditional_probability)
    assert list(result.minimization.initial_guess.keys()) == [
        "P000",
        "P001",
        "P010",
        "P011",
        "P100",
        "P101",
        "P110",
        "P111",
    ]
    assert list(result.minimization.initial_guess.values()) == [1.0 / 8] * 8


def test_validate_config(config_conditional_probability):
    config = validate.parse_config(config_conditional_probability)
    assert validate.validate_config(config)


def test_validate_joint_distributions_success():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
    )
    assert validate._validate_joint_distributions(config)


def test_validate_joint_distributions_fail_not_proper_format():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
        ],
    )
    config = Config(
        ["Pijk", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
    )
    assert not validate._validate_joint_distributions(config)


def test_validate_joint_distributions_fail_not_proper_tag():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
        ],
    )
    config = Config(
        ["A000", "A001", "A010", "A011", "A100", "A101", "A110", "A111"],
    )
    assert not validate._validate_joint_distributions(config)


def test_validate_joint_distributions_fail_missing_states():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
        ],
    )
    config = Config(
        ["P001", "P010", "P011", "P100", "P101", "P110", "P111"],
    )
    assert not validate._validate_joint_distributions(config)


def test_validate_joint_distributions_fail_wrong_state():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
        ],
    )
    config = Config(
        ["P001", "P001", "P010", "P011", "P10", "P101", "P110", "P111"],
    )
    assert not validate._validate_joint_distributions(config)


def test_validate_assessments_success():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "assessments",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        {
            "P.01": 0.4643,
            "P.11": 0.2411,
            "P1.1": 0.3490,
            "P00.": 0.1988,
            "P01.": 0.2463,
            "P10.": 0.3017,
            "P11.": 0.2532,
        },
    )
    assert validate._validate_joint_distributions(config)


def test_validate_assessments_fail_missing_marginalization():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "assessments",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        {
            "P01": 0.4643,
            "P.11": 0.2411,
            "P1.1": 0.3490,
            "P00.": 0.1988,
            "P01.": 0.2463,
            "P10.": 0.3017,
            "P11.": 0.2532,
        },
    )
    assert not validate._validate_assessments(config)


def test_validate_assessments_fail_not_proper_tag():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "assessments",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        {
            "A.01": 0.4643,
            "B.11": 0.2411,
            "A1.1": 0.3490,
            "P00.": 0.1988,
            "P01.": 0.2463,
            "P10.": 0.3017,
            "P11.": 0.2532,
        },
    )
    assert not validate._validate_assessments(config)


def test_validate_assessments_fail_wrong_format():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "assessments",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        {
            "P.01": 0.4643,
            "P.1a": 0.2411,
            "P1.1": 0.3490,
            "P00.": 0.1988,
            "P01.": 0.2463,
            "P10.": 0.3017,
            "P11.": 0.2532,
        },
    )
    assert not validate._validate_assessments(config)


def test_validate_assessments_fail_wrong_state():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "assessments",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        {
            "P.01": 0.4643,
            "P.11": 0.2411,
            "P2.1": 0.3490,
            "P00.": 0.1988,
            "P01.": 0.2463,
            "P10.": 0.3017,
            "P11.": 0.2532,
        },
    )
    assert not validate._validate_assessments(config)


def test_number_of_variables_success():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "assessments",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        {
            "P.01": 0.4643,
            "P.11": 0.2411,
            "P1.1": 0.3490,
            "P00.": 0.1988,
            "P01.": 0.2463,
            "P10.": 0.3017,
            "P11.": 0.2532,
        },
    )
    assert validate.number_of_variables(config) == 3


def test_number_of_variables_fail():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "assessments",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"], {"P.1": 0.4643}
    )
    assert validate.number_of_variables(config) == -1


def test_validate_conditioned_variables_success():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "conditioned_variables",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        [],
    )
    assert validate._validate_conditioned_variables(config)

    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        [1, 2],
    )
    assert validate._validate_conditioned_variables(config)


def test_validate_conditioned_variables_fail_duplicate_variables():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "conditioned_variables",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        [1, 1],
    )
    assert not validate._validate_conditioned_variables(config)


def test_validate_conditioned_variables_fail_wrong_variables():
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "conditioned_variables",
        ],
    )
    config = Config(
        ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"],
        [1, 3],
    )
    assert not validate._validate_conditioned_variables(config)


def test_validate_minimization_success():
    joint_distribution = ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"]
    Minimization = namedtuple("minimization", ["initial_guess", "bounds"])
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "minimization",
        ],
    )
    minimization = Minimization(
        None,
        None,
    )
    config = Config(
        joint_distribution,
        minimization,
    )
    assert validate._validate_minimization(config)

    minimization = Minimization(
        {
            "P000": 0.015,
            "P001": 0.04,
            "P010": 0.01,
            "P011": 0.2,
            "P100": 0.02,
            "P101": 0.3,
            "P110": 0.2,
            "P111": 0.05,
        },
        {
            "P000": [0.015, 1.0],
            "P001": [0.03, 1],
            "P010": [0, 1],
            "P011": [0, 1],
            "P100": [0, 0.021],
            "P101": [0, 1],
            "P110": [0, 1],
            "P111": [0, 1],
        },
    )
    config = Config(
        joint_distribution,
        minimization,
    )
    assert validate._validate_minimization(config)


def test_validate_minimization_fail_not_same_probabilities_bounds():
    joint_distribution = ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"]
    Minimization = namedtuple("minimization", ["initial_guess", "bounds"])
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "minimization",
        ],
    )
    minimization = Minimization(
        {
            "P000": 0.015,
            "P001": 0.04,
            "P010": 0.01,
            "P100": 0.02,
            "P101": 0.3,
            "P110": 0.2,
            "P111": 0.05,
        },
        {
            "P000": [0.015, 1.0],
            "P001": [0.03, 1],
            "P010": [0, 1],
            "P011": [0, 1],
            "P100": [0, 0.021],
            "P101": [0, 1],
            "P110": [0, 1],
            "P111": [0, 1],
        },
    )
    config = Config(
        joint_distribution,
        minimization,
    )
    assert not validate._validate_minimization(config)


def test_validate_minimization_fail_not_same_probabilities_initial_guess():
    joint_distribution = ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"]
    Minimization = namedtuple("minimization", ["initial_guess", "bounds"])
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "minimization",
        ],
    )
    minimization = Minimization(
        {
            "P000": 0.015,
            "P001": 0.04,
            "P010": 0.01,
            "P011": 0.2,
            "P100": 0.02,
            "P101": 0.3,
            "P110": 0.2,
            "P111": 0.05,
        },
        {
            "P000": [0.015, 1.0],
            "P001": [0.03, 1],
            "P010": [0, 1],
            "P011": [0, 1],
            "P100": [0, 0.021],
            "P101": [0, 1],
            "P111": [0, 1],
        },
    )
    config = Config(
        joint_distribution,
        minimization,
    )
    assert not validate._validate_minimization(config)


def test_validate_minimization_fail_not_same_probabilities_bounds_not_in_zero_one():
    joint_distribution = ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"]
    Minimization = namedtuple("minimization", ["initial_guess", "bounds"])
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "minimization",
        ],
    )
    minimization = Minimization(
        {
            "P000": 0.015,
            "P001": 0.04,
            "P010": 0.01,
            "P011": 0.2,
            "P100": -10.0,
            "P101": 0.3,
            "P110": 0.2,
            "P111": 0.05,
        },
        {
            "P000": [0.015, 1.0],
            "P001": [0.03, 1],
            "P010": [0, 1],
            "P011": [0, 1],
            "P100": [0, 0.021],
            "P101": [0, 1],
            "P110": [0, 1],
            "P111": [0, 1],
        },
    )
    config = Config(
        joint_distribution,
        minimization,
    )
    assert not validate._validate_minimization(config)


def test_validate_minimization_fail_initial_guess_not_in_zero_one():
    joint_distribution = ["P000", "P001", "P010", "P011", "P100", "P101", "P110", "P111"]
    Minimization = namedtuple("minimization", ["initial_guess", "bounds"])
    Config = namedtuple(
        "Config",
        [
            "joint_distributions",
            "minimization",
        ],
    )
    minimization = Minimization(
        {
            "P000": 0.015,
            "P001": 0.04,
            "P010": 0.01,
            "P011": 0.2,
            "P100": 0.02,
            "P101": 0.3,
            "P110": 0.2,
            "P111": 0.05,
        },
        {
            "P000": [0.015, 1.0],
            "P001": [0.03, 1],
            "P010": [0, 1],
            "P011": [0, 1],
            "P100": [0, 10],
            "P101": [0, 1],
            "P110": [0, 1],
            "P111": [0, 1],
        },
    )
    config = Config(
        joint_distribution,
        minimization,
    )
    assert not validate._validate_minimization(config)
