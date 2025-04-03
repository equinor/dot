import re
from typing import Any

import numpy as np

from ..errors import (
    DiscreteConditionalProbabilityFunctionValidationError,
    DiscreteProbabilityVariableValidationError,
    DiscreteUnconditionalProbabilityFunctionValidationError,
    )


def discrete_variables(arg: Any) -> dict:
    if not isinstance(arg, dict):
        raise DiscreteProbabilityVariableValidationError(arg)
    if not all([isinstance(v, (list, np.ndarray)) for v in arg.values()]):
        raise DiscreteProbabilityVariableValidationError(arg)
    try:
        if any(max(np.asarray(v).shape) != np.asarray(v).size for v in arg.values()):
            pass
    except Exception as e:
        raise DiscreteProbabilityVariableValidationError(e)
    if any(max(np.asarray(v).shape) != np.asarray(v).size for v in arg.values()):
        raise DiscreteProbabilityVariableValidationError((arg))
    # remove white spaces as the string is used as variable name by xarray
    return {re.sub(r"\s+", "_", k): v for k, v in arg.items()}


def discrete_conditional_probability_function(
        arg: Any,
        conditioned_variables: dict,
        conditioning_variables: dict
        ) -> dict:
    def isnormalized(arr, cond_variables, threshold=1e-6):
        axis = tuple(a for a in range(len(cond_variables.keys())))
        return np.all(np.linalg.norm(arr.sum(axis=axis) - 1.0) < threshold)

    if not isinstance(arg, np.ndarray):
        raise DiscreteConditionalProbabilityFunctionValidationError(arg)

    variables = {**conditioned_variables, **conditioning_variables}
    has_consistent_shape = tuple(
        [len(v) for v in variables.values()]
        ) == np.asarray(arg).shape
    is_all_nans = np.isnan(arg).all()
    is_between_zero_and_one = np.all(np.logical_and(arg >= 0, arg <= 1))
    is_normalized = isnormalized(arg, conditioned_variables)

    if not has_consistent_shape:
        raise DiscreteConditionalProbabilityFunctionValidationError(arg)

    if not (is_all_nans ^ is_between_zero_and_one):
        raise DiscreteConditionalProbabilityFunctionValidationError(arg)

    if not (is_all_nans ^ is_normalized):
        raise DiscreteConditionalProbabilityFunctionValidationError(arg)

    return arg


def discrete_unconditional_probability_function(
        arg: Any,
        variables: dict
        ) -> dict:
    def isnormalized(arr, threshold=1e-6):
        return np.all(np.linalg.norm(arr.sum() - 1.0) < threshold)

    if not isinstance(arg, np.ndarray):
        raise DiscreteUnconditionalProbabilityFunctionValidationError(arg)

    has_consistent_shape = tuple(
        [len(v) for v in variables.values()]
        ) == np.asarray(arg).shape
    is_all_nans = np.isnan(arg).all()
    is_between_zero_and_one = np.all(np.logical_and(arg >= 0, arg <= 1))
    is_normalized = isnormalized(arg)

    if not has_consistent_shape:
        raise DiscreteUnconditionalProbabilityFunctionValidationError(arg)

    if not (is_all_nans ^ is_between_zero_and_one):
        raise DiscreteUnconditionalProbabilityFunctionValidationError(arg)

    if not (is_all_nans ^ is_normalized):
        raise DiscreteUnconditionalProbabilityFunctionValidationError(arg)

    return arg
