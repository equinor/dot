"""
The approach is based on these papers

Abbas A. E. (2006) Entropy Methods for Joint Distributions in Decision Analysis,
IEEE TRANSACTIONS ON ENGINEERING MANAGEMENT, VOL. 53, NO. 1, 146 - 159

Bratvold, R. B., S. H. Begg, S. Rasheva (2010) A New Approach to Uncertainty
Quantification for Decision Making, SPE 130157, DOI: 10.2118/130157-MS


The approach is valid for pair-wise constraints.

It uses the dot notation introduced by Abbas (2006): Probabilities are represented
by a capital P followed by indices. The indices represents the index of the variable
outcomes. Dots in the list of indices represents the summation (marginalization) over
these variables.
For example the probability P with 2 outcomes Peach or Lemon would be
    P1 for Peach
    P2 for Lemon
    P. for the marginal distribution
For P (A={a1, a2}, B={b1, b2, b3}, C={c1, c2})
    P231 is P(A=a2, B=b3, C=c1)
    P2.. is P(A=a2) = P(A=a2, B=b1+b2+b3, C=c1+c2)

Conditional probabilities can be estimated by
    P(A|B) = P(A,B)/P(B)
    P(A|B,C,D) = P(A,B,C,D)/P(B,C,D)
    P(A,B|C,D) = P(A,B,C,D)/P(C,D)

With the above notations
    P(A|B,C) = P(A,B,C)/P(B,C)
             = Pikj/P.jk

WARNING:
This notation actually implies a one digit number associated to a given state of the
probability.
This means probabilities can have at most 10 outcomes (from 0 to 9)
"""

import json
import re
from collections import namedtuple
from copy import deepcopy
from itertools import compress

import numpy as np
from numpy.typing import ArrayLike
from scipy.optimize import minimize

from . import validate
from .common import PROBABILITY_TAG, logger


def probabilities_per_assessment(
    joint_distributions: list[str], assessments: dict[str, float]
) -> dict[str, list[int]]:
    """Look for probabilities contributing to assessment

    Args
        joint_distributions (list[str]): the list of joint distribution names
        assessments (dict[str, float]): the list of assessments

    Return
        dict[str, list[int]]: list of integer list.
    """
    return {
        item1: {
            "distributions": [
                item2 for item2 in joint_distributions if re.match(item1, item2)
            ],
            "indices": [
                k
                for k, item2 in enumerate(joint_distributions)
                if re.match(item1, item2)
            ],
        }
        for item1 in assessments
    }


def marginalization_constraints(
    marginalization_indices: dict, assessments: dict
) -> list[dict]:
    """Create the equality constraints for the minimization operator due to
    the marginalization given through the assessments and the join distributions values

    Args
        marginalization_indices (dict): dictionary representing the proability
        summations assessments (dict[str, float]): the list of assessments

    Return
        list[dict]: a list of dictionaries representing the equality constraints.
        One item per constraints.
    """
    constraints = []
    for summation in marginalization_indices.keys():
        cstring = ""
        for ind in marginalization_indices[summation]["indices"]:
            cstring += "x[" + str(ind) + "]+"
        cstring = cstring[:-1] + "-" + str(assessments[summation])
        constraints.append({"type": "eq", "fun": eval("lambda x: " + cstring)})  # noqa {S307}  # nosec
        logger.debug(f" Marginalization: {cstring}")
    return constraints


def replace_p_with_x(input_string: str) -> str:
    """Replace occurrences of 'P' in the input string with 'x' if 'P'
    is preceded by any of the characters '(', '+', '-', '/', or '*'
    and followed by any of the characters ')', '*', '/', '+', or '-'.

    Args:
        input_string (str): The input string containing the text to process.

    Returns:
        str: A new string with 'P' replaced by 'x' based on the specified conditions.

    Examples:
        >>> replace_p_with_x("A + P - B * (P / C) + D * P")
        'A+x-B*(x/C)+D*P'

        >>> replace_p_with_x("No replacement for P here")
        'NoreplacementforPhere'
    """
    pattern = r"(?<=[\(\+\-\*/])P(?=[\)\*\+\-\/])"
    return re.sub(pattern, "x", input_string.replace(" ", ""))


def replace_pijk_with_x_indexed(input_string: str, replacements: list) -> str:
    """Transform all occurrences of specified elements in the input string
    into an x variable with corresponding indices in the provided list.

    Each occurrence of an element from the list will be replaced
    by a variable withindex given by the index of the element in the list.
    If an element is not found in the list, it remains unchanged.

    Args:
        input_string (str): The string to transform.
        replacements (list): The list of elements to be replaced by their indices.

    Returns:
        str: The transformed string with elements replaced by their indices.

    Examples:
        >>> replace_pijk_with_x_indexed(
        ... "AA is BB or AA in CC but not A, B or C", ["AA", "BB", "CC"])
        '0 is 1 or 0 in 2 but not A, B or C'

        >>> replace_pijk_with_x_indexed("Hello World", ["Hello", "World"])
        'x[0]x[1]'
    """

    def replace_with_index(match):
        return f"x[{str(replacements.index(match.group(0)))}]"

    pattern = r"\b(" + "|".join(map(re.escape, replacements)) + r")\b"
    return re.sub(pattern, replace_with_index, input_string).replace(" ", "")


def _parse_constraint(cstring: str, distributions: list[float]) -> str:
    """Parse a constraint as a string interpretable by a lambda function

    Args
        cstring (str): the constraint expressed in terms of the joint probabilities
        distributions (list[float]): the list of joint distribution names

    Return
        str: the constraint expressed in term of the variable x.
    """
    relations = ["=", ">=", "<="]
    used_filter = [delim in cstring for delim in relations]
    if not any(used_filter):
        logger.critical(
            f"Constraints {cstring} should have one of the relations {relations}, "
            "and only once."
        )
        raise ValueError(
            f"Constraints {cstring} should have one of the relations {relations}, "
            "and only once."
        )

    logger.debug(f" Relation: {relations} {used_filter}")
    relation = list(compress(relations, used_filter))[-1]
    if cstring.count(relation) != 1:
        logger.critical(
            f"Constraints {cstring} should have one of the relations {relations}, "
            "and only once."
        )
        raise ValueError(
            f"Constraints {cstring} should have one of the relations {relations}, "
            "and only once."
        )
    logger.debug(f" Relation: {relation}")
    substrings = cstring.partition(relation)
    constraint = f"{substrings[0]} - ({substrings[2].strip()})"
    if relation == "<=":
        constraint = f"-({constraint})"
    logger.debug(f" Constraints: {constraint}")
    clambda = replace_pijk_with_x_indexed(constraint, distributions)
    clambda = replace_p_with_x(clambda)
    logger.debug(f" For lambda function: {clambda}")
    return clambda


def equality_constraints(constraints: list[str], distributions: list[float]) -> list:
    """parse all equality constraints into a format interpretable by the minimization

    Args:
        constraints (list[str]): the constraints expressed in terms of the joint
        probabilities distributions (list[float]): the list of joint distribution names

    Return:
        list[dict]: the equality constraints in a format interpretable by the
        minimization
    """
    if not constraints:
        return []
    return [
        {
            "type": "eq",
            "fun": eval(  # noqa {S307} # nosec
                "lambda x: " + _parse_constraint(cstring, distributions)
            ),
        }
        for cstring in constraints
    ]


def inequality_constraints(constraints, distributions) -> list:
    """parse all inequality constraints into a format interpretable by the minimization

    Args:
        constraints (list[str]): the constraints expressed in terms of the joint
        probabilities distributions (list[float]): the list of joint distribution names

    Return:
        list[dict]: the inequality constraints in a format interpretable by the
        minimization
    """
    if not constraints:
        return []
    return [
        {
            "type": "ineq",
            "fun": eval(  # noqa {S307} # nosec
                "lambda x: " + _parse_constraint(cstring, distributions)
            ),
        }
        for cstring in constraints
    ]


def all_constraints(config: namedtuple) -> list:
    """make a list of all constraints

        It includes the marginalization, and the optional equality constraints
        and inequality constraints

    Arg
        config (namedtuple): the configuration of the constraints

    Return
        list: the list of the constraints in proper format for the minimization
    """
    marginalization_indices = probabilities_per_assessment(
        config.joint_distributions, config.assessments
    )
    logger.debug(f"Marginalization = \n{json.dumps(marginalization_indices, indent=2)}")
    marginalization = marginalization_constraints(
        marginalization_indices, config.assessments
    )
    eq_constraints = equality_constraints(config.equality, config.joint_distributions)
    ineq_constraints = inequality_constraints(
        config.inequality, config.joint_distributions
    )
    constraints = marginalization + eq_constraints + ineq_constraints
    logger.debug(f"Constraints: \n{constraints}")
    return constraints


def maximize_entropy(*, constraints: list, P0: ArrayLike, bnds: tuple):
    """estimation of the joint distributions by maximizing the entropy

    Args
        constraints (list): the constraints (see scipy.minimize for format)
        P0 (ArrayLike): initial guess of the marginal distributions.
        bnds (tuple): Boundaries in which the solution lies.

    Return:
        scipy.OptimizeResult: the result of the minimization
    """

    def minus_entropy(x: float):
        # -H (entropy is defined as the negative form)
        return np.sum(x * np.log(x))

    return minimize(
        minus_entropy,
        np.asarray(P0).ravel(),
        method="SLSQP",
        bounds=np.asarray(bnds),
        constraints=constraints,
    )


def solve_joint_probability(config: namedtuple) -> dict:
    """Estimate the joint probability by minimizing the MEP

    Arg
        config (namedtuple): the configuration of the constraints

    Returns
        dict[str, float]: the joint probability
    """
    constraints = all_constraints(config)
    result = maximize_entropy(
        constraints=constraints,
        P0=list(config.minimization.initial_guess.values()),
        bnds=list(config.minimization.bounds.values()),
    )
    logger.info(f"Results: \n {result}")
    return dict(zip(config.joint_distributions, result.x.tolist(), strict=False))


def get_marginal_distribution(config: namedtuple) -> list:
    """Estimate the marginal distribution from a higher dimension one

    Arg
        config (namedtuple): the configuration of the constraints

    Returns
        list: the elements of the probability to sum for estimating the
        desired marginal distribution
    """
    marginal_distributions = []
    for item in config.joint_distributions:
        item_as_list = list(item)
        for index in config.conditioned_variables:
            logger.debug(
                f"item: {item} {len(PROBABILITY_TAG)} "
                "{index} {item[len(PROBABILITY_TAG)+index]}"
            )
            item_as_list[len(PROBABILITY_TAG) + index] = "."
        marginal_distributions.append("".join(item_as_list))
    return list(set(marginal_distributions))


def to_conditional_probability(config: namedtuple, x0: dict) -> dict:
    """Convert the joint distribution into a conditional one

        It uses
            P(A|B,C) = P(A,B,C)/P(B,C)
                     = Pikj/P.jk

    Args
        config (namedtuple): the configuration of the constraints
        x0 (dict[str, float]): the joint probability

    Return
        dict[str, float]: the conditional probability
    """
    marginal_distributions = get_marginal_distribution(config)
    logger.debug(f"Marginal distributions: {marginal_distributions}")
    marginalization_indices = probabilities_per_assessment(
        config.joint_distributions, marginal_distributions
    )
    logger.debug(
        f"marginalization_indices: \n{json.dumps(marginalization_indices, indent=2)}"
    )
    x = deepcopy(x0)
    for p in marginalization_indices.keys():
        logger.debug(f"{x} {p}")
        denominator = np.sum(
            np.asarray([x[key] for key in marginalization_indices[p]["distributions"]])
        )
        for key in marginalization_indices[p]["distributions"]:
            logger.debug(f" {key} {x[key]} {denominator} {x[key]/denominator}")
            x[key] /= denominator
    # convert to native python types (float)
    x = dict(zip(x.keys(), [val.item() for val in x.values()], strict=False))
    return x


def solve(config: namedtuple) -> ArrayLike:
    """Estimate the MEP for the given configuration

    Args:
        config (namedtuple): Configuration describing the probability to estmate

    Returns:
        ArrayLike: Estimated probability
    """
    x0 = solve_joint_probability(config)
    if config.conditioned_variables:
        x0 = to_conditional_probability(config, x0)
    return x0


def mep(config_dict: dict) -> ArrayLike:
    """Estimate a joint or conditional probability using MEP

    Args:
        config_dict (dict): Configuration for the MEP

    Returns:
        ArrayLike: The estimated probability
    """
    if not validate.validate_input_dictionary(config_dict):
        logger.critical(
            "Input dictionary for configuration does not have the correct keys."
        )
        raise ValueError
    config = validate.parse_config(config_dict)
    if not validate.validate_config(config):
        logger.critical("Configuration does not follow (some of) expectations.")
        raise ValueError
    return solve(config)
