from itertools import product

import numpy as np
import xarray as xr
from numpy.typing import ArrayLike

from src.v0.services.classes.abstract_probability import ProbabilityABC

from .validations import validate_and_set_probability


class DiscreteUnconditionalProbability(ProbabilityABC):
    """DiscreteUnconditionalProbability"""

    def __init__(self, probability_function: ArrayLike, variables: dict) -> None:
        """
         Parameters
         -----------
         probability_function: ArrayLike
             gives the probability that a variable is equal to some value
         variables: dict
             involves the variable name and its values; values refers to the set of possible outcomes

         Warning
         --------
             Spaces in variable names and values will be removed.

         Notes
         -----

         For the Probability P(A, B , C) such as

                || 1. B  ||    b1       b1   |   b2     b2
                || 2. C  ||    c1   |   c2   |   c1  |  c1
        -----------------------------------------------------------------
         0. A   ||       ||         |        |       |
        -----------------------------------------------------------------
         a1     ||       ||   0.00  |  0.13  |  0.20 |  0.06
         a2     ||       ||   0.03  |  0.28  |  0.11 |  0.02
         a3     ||       ||   0.12  |  0.04  |  0.10 |  0.01

         the probability_function will be
             [
                 [0.00, 0.13, 0.20, 0.06],
                 [0.03, 0.18, 0.11, 0.02],
                 [0.12, 0.04, 0.10, 0.01],
             ]

         and the variables
             {
                 "A": ["a1", "a2", "a3"],
                 "B": ["b1", "b2"],
                 "C": ["c1", "c2"],
             }
        """
        super().__init__()
        variables = validate_and_set_probability.discrete_variables(variables)
        probability_function = validate_and_set_probability.discrete_unconditional_probability_function(
            probability_function, variables
        )
        self._cpt = xr.DataArray(probability_function, coords=variables)

    @property
    def outcomes(self):
        variable_names = self._cpt.dims
        if len(variable_names) == 1:
            return tuple(self._cpt.coords[variable_names[0]].data.tolist())
        else:
            return tuple(product(*tuple(tuple(self._cpt.coords[vn].data.tolist()) for vn in variable_names)))

    @property
    def variables(self):
        return self._cpt.dims

    @classmethod
    def initialize_nan(cls, variables: dict):
        data_shape = tuple(np.asarray(v).shape[0] for v in variables.values())
        data = np.full(data_shape, np.nan)
        return cls(data, variables=variables)

    @classmethod
    def initialize_uniform(cls, variables: dict):
        data_shape = tuple(np.asarray(v).shape[0] for v in variables.values())
        data = np.ones(data_shape) / np.prod(data_shape)
        return cls(data, variables=variables)

    def get_distribution(self, **variables):
        """Return the probability distribution

        Parameters
        ----------
        **variables:
            variables (name=value) for which the distribution is desired

        Return
        ------
        xr.DataArray
        """
        return self._cpt.sel(**variables)
