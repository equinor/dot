import itertools
import json
from collections import namedtuple
from pathlib import Path

import numpy as np

from .common import PROBABILITY_TAG, Configuration, Minimization, logger


def validate_input_dictionary(config: dict) -> bool:
    """Check that keys in the dictionary are as expected

    Args:
        config (namedtuple): configuration

    Returns:
        bool: True if configuration is valid
    """
    valid = False
    if set(config.keys()) != {
        "joint_distributions",
        "assessments",
        "equality",
        "inequality",
        "conditioned_variables",
        "minimization",
    }:
        logger.critical("Keys of input dictionary (configuration) are not as expected")
        return valid
    if set(config["minimization"].keys()) != {"initial_guess", "bounds"}:
        logger.critical("Keys of input dictionary (configuration) are not as expected")
        return valid
    return True


def parse_config(config: dict) -> namedtuple:
    """Parse configuration dictionary

    Args
        config (dict): configuration

    Return
        namedtuple: the configuration as a named tuple
    """
    problem_size = len(config["joint_distributions"])
    logger.debug(f"Size of problem {problem_size}")

    initial_guess = (
        dict(
            zip(
                config["joint_distributions"],
                (np.ones((problem_size,)) / problem_size).tolist(),
                strict=False,
            )
        )
        if not config["minimization"]["initial_guess"]
        else {
            k: config["minimization"]["initial_guess"][k]
            for k in config["joint_distributions"]
        }
    )
    bounds = (
        dict(
            zip(config["joint_distributions"], [(0.0, 1.0)] * problem_size, strict=False)
        )
        if not config["minimization"]["bounds"]
        else {
            k: config["minimization"]["bounds"][k] for k in config["joint_distributions"]
        }
    )

    minimization = Minimization(
        initial_guess,
        bounds,
    )

    config = Configuration(
        config["joint_distributions"],
        config["assessments"],
        config["equality"],
        config["inequality"],
        config["conditioned_variables"],
        minimization,
    )

    logger.debug(f"\n{config}")
    return config


def _validate_joint_distributions(config: namedtuple) -> bool:
    """validate the format of the joint distributions

    Args:
        config (namedtuple): configuration

    Returns:
        bool: True if configuration is valid
    """
    valid = False
    if not all(item.startswith(PROBABILITY_TAG) for item in config.joint_distributions):
        logger.critical(
            "Not all items of the joint distributions start with the "
            "correct tag ({PROBABILITY_TAG})"
        )
        return valid
    if not all(
        item[len(PROBABILITY_TAG) :].isnumeric() for item in config.joint_distributions
    ):
        logger.critical(
            "Not all items of the joint distributions only contain digits "
            "after the tag (e.g. {PROBABILITY_TAG}0210)"
        )
        return valid
    if len(set(map(len, config.joint_distributions))) != 1:
        logger.critical("Not all items of the joint distributions have the same length")
        return valid

    # a bit complicated as if the first variable only has one outcome it will start by 0
    # so we need to find the codes of all outcomes, add 1 to each variables to know how
    # many states they each have then find the maximum number (total number of outcomes)
    # and then check if the input has as many
    states_count_per_variable = [
        item[len(PROBABILITY_TAG) :] for item in config.joint_distributions
    ]
    states_count_per_variable = [
        "".join([str(int(digit) + 1) for digit in item])
        for item in states_count_per_variable
    ]
    last_states_count = max([int(item) for item in states_count_per_variable])
    total_states_count = np.prod(np.array(list(map(int, str(last_states_count)))))
    if len(config.joint_distributions) != total_states_count:
        logger.critical("Some obvious joint distributions are missing")
        return valid

    return True


def number_of_variables(config: namedtuple) -> int:
    """Estimate the number of variables in the problem

    Args
        config (namedtuple): configuration

    Return
        int: the number of variables
    """
    count = set(
        [len(item) for item in config.joint_distributions]
        + [len(key) for key in config.assessments]
    )

    if len(count) != 1:
        return -1

    variables_count = list(count)[0] - len(PROBABILITY_TAG)
    logger.debug(f"Number of variables = {variables_count}")

    return variables_count


def _validate_assessments(config: namedtuple) -> bool:
    """validate the format of the assessments

    Args:
        config (namedtuple): configuration

    Returns:
        bool: True if configuration is valid
    """
    valid = False
    if not all(item.startswith(PROBABILITY_TAG) for item in config.assessments.keys()):
        logger.critical(
            "Not all keys of the assessments start with the "
            "correct tag ({PROBABILITY_TAG})"
        )
        return valid
    if not all(
        item[len(PROBABILITY_TAG) :].replace(".", "").isnumeric()
        for item in config.assessments.keys()
    ):
        logger.critical(
            "Not all keys of the assessments only contain digits or '.' after "
            "the tag (e.g. {PROBABILITY_TAG}.210)"
        )
        return valid
    if len(set(map(len, config.assessments.keys()))) != 1:
        logger.critical("Not all keys of the assessments have the same length")
        return valid
    if number_of_variables(config) == -1:
        logger.critical(
            "Format of pair-wise assessments and desired probabilities is not correct"
        )
        return valid

    # a bit complicated as if the first variable only has one outcome it will start by 0
    # so we need to find the codes of all outcomes, add 1 to each variables to know how
    # many states they each have then find the maximum number (total number of outcomes)
    # and then check if the input has as many
    states_count_per_variable_joint = [
        item[len(PROBABILITY_TAG) :] for item in config.joint_distributions
    ]
    states_count_per_variable_joint = [
        "".join([str(int(digit) + 1) for digit in item])
        for item in states_count_per_variable_joint
    ]
    last_states_count_joint = max(
        [int(item) for item in states_count_per_variable_joint]
    )

    states_assessments = [item[len(PROBABILITY_TAG) :] for item in config.assessments]
    dot_position = [item.index(".") for item in states_assessments]
    for k, v in zip(dot_position, states_assessments, strict=False):
        relevant_max_states = list(
            str(last_states_count_joint)[:k] + str(last_states_count_joint)[k + 1 :]
        )
        relevant_assessments = list(v.replace(".", ""))
        if any(
            int(assessment) >= int(joint)
            for assessment, joint in zip(
                relevant_assessments, relevant_max_states, strict=False
            )
        ):
            logger.critical("An assessment is trying to marginalize using unknown state")
            return valid

    return True


def _validate_conditioned_variables(config: namedtuple) -> bool:
    """validate the format of the conditioned_variables

    Args:
        config (namedtuple): configuration

    Returns:
        bool: True if configuration is valid
    """
    if not config.conditioned_variables:
        return True

    valid = False
    if len(config.conditioned_variables) != len(set(config.conditioned_variables)):
        logger.critical("Given condiotioned variables are not unique")
        return valid
    if max(config.conditioned_variables) >= len(
        config.joint_distributions[0][len(PROBABILITY_TAG) :]
    ):
        logger.critical(
            "Input a conditioning variable not consistent with the joint distributions"
        )
        return valid

    return True


def _validate_minimization_bounds(config: namedtuple) -> bool:
    """validate the format of the minimization (bounds)

    Args:
        config (namedtuple): configuration

    Returns:
        bool: True if configuration is valid
    """
    valid = False
    if not config.minimization.bounds:
        return True
    if set(config.minimization.bounds.keys()) != set(config.joint_distributions):
        logger.critical(
            "Keys defining the optimization bounds are not consistent with "
            "the joint_distribution"
        )
        return valid
    if any(
        np.abs(item) > 1
        for item in set(itertools.chain(*config.minimization.bounds.values()))
    ):
        logger.critical("Some optimization bounds not in 0..1 interval")
        return valid
    return True


def _validate_minimization_initial_guess(config: namedtuple) -> bool:
    """validate the format of the minimization (initial_guess)

    Args:
        config (namedtuple): configuration

    Returns:
        bool: True if configuration is valid
    """
    valid = False
    if not config.minimization.initial_guess:
        return True
    if set(config.minimization.initial_guess.keys()) != set(config.joint_distributions):
        logger.critical(
            "Keys defining the optimization initial_guess are not consistent with "
            "the joint_distribution"
        )
        return valid
    if any(np.abs(item) > 1 for item in config.minimization.initial_guess.values()):
        logger.critical("Some optimization initial guess not in 0..1 interval")
        return valid
    return True


def _validate_minimization(config: namedtuple) -> bool:
    """validate the format of the minimization

    Args:
        config (namedtuple): configuration

    Returns:
        bool: True if configuration is valid
    """
    if not _validate_minimization_initial_guess(config):
        return False
    if not _validate_minimization_bounds(config):
        return False
    return True


def validate_config(config: namedtuple) -> bool:
    """Validation of the configuration

    Args:
        config (namedtuple): configuration

    Returns:
        bool: True if configuration is valid
    """
    valid = False
    if not _validate_joint_distributions(config):
        return valid
    if not _validate_assessments(config):
        return valid
    if not _validate_conditioned_variables(config):
        return valid
    if not _validate_minimization(config):
        return valid
    return True


def read_config(config_file: Path) -> dict:
    """Read the json config file

    Args:
        config_file (Path): json file for configuration

    Returns:
        dict: _the ocnfiguration as a dictionary
    """
    with open(config_file) as f:
        config_dict = json.load(f)
    return config_dict
