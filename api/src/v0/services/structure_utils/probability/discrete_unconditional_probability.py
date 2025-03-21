import json
import logging
import re
from itertools import product

import numpy as np
import xarray as xr
from numpy.typing import ArrayLike

from ..probability.abstract_probability import ProbabilityABC

logger = logging.getLogger(__name__)


class VariableNot1D(Exception):
    def __init__(self):
        error_message = "One of the variables cannot be interpreted as 1D"
        super().__init__(error_message)
        logger.critical(error_message)


class CPTTypeError(Exception):
    def __init__(self, cpt_type):
        error_message = (
            f"Expected DiscreteUnconditionalProbability dtype, got {cpt_type}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class AgrumConversionError(Exception):
    def __init__(self):
        error_message = "pyAgrum only takes 1D variables in UncertaintyNode"
        super().__init__(error_message)
        logger.critical(error_message)


class DiscreteUnconditionalProbability(ProbabilityABC):
    """DiscreteUnconditionalProbability"""

    def __init__(self, probability_function: ArrayLike, variables: dict) -> None:
        """
         Parameters
         -----------
         probability_function: ArrayLike
             gives the probability that a variable is equal to some value
         variables: dict
             involves the variable name and its values; values refers to the set of
             possible outcomes

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
        if any(
            max(np.asarray(v).shape) != np.asarray(v).size for v in variables.values()
        ):
            raise VariableNot1D
        variables = {re.sub(r"\s+", "", k): v for k, v in variables.items()}
        self._cpt = xr.DataArray(probability_function, coords=variables)

    @property
    def outcomes(self):
        variable_names = self._cpt.dims
        if len(variable_names) == 1:
            return tuple(self._cpt.coords[variable_names[0]].data.tolist())
        else:
            return tuple(
                product(
                    *tuple(
                        tuple(self._cpt.coords[vn].data.tolist())
                        for vn in variable_names
                    )
                )
            )

    @property
    def variables(self):
        return self._cpt.dims

    @classmethod
    def from_db_model(cls, data):
        array_size = tuple([len(v) for v in data.variables.values()])
        distribution = np.reshape(data.probability_function, array_size)
        return cls(distribution, data.variables)

    @classmethod
    def initialize_nan(cls, variables: dict):
        data_shape = tuple(np.asarray(v).shape[0] for v in variables.values())
        return cls(np.full(data_shape, np.nan), variables=variables)

    def set_to_uniform(self):
        data_shape = tuple(np.asarray(v).shape[0] for v in self._cpt.coords.values())
        self._cpt.data = np.ones(data_shape) / np.prod(data_shape)
        return self

    # does it even make sense to normalize?
    def normalize(self):
        # normalize columwise before normalizing wrt the whole matrix?
        # self._cpt = np.apply_over_axes(np.sum, self._cpt, range(1, self._cpt.ndim))
        self._cpt = self._cpt / self._cpt.sum()
        return self

    def isnormalized(self, threshold=1e-6):
        return np.all(np.linalg.norm(self._cpt.sum() - 1.0) < threshold)

    @classmethod
    def from_json(cls, json_str: str):
        d = json.loads(json_str)
        if d["dtype"] != cls.__name__:
            raise CPTTypeError(d["dtype"])
        return cls(d["probability_function"], d["variables"])

    def to_json(self):
        return json.dumps(self.to_dict())

    def to_dict(self):
        d_ = self._cpt.to_dict()
        pf = np.array(d_["data"])
        d = {
            "dtype": self.__class__.__name__,
            "probability_function": np.reshape(pf, (pf.shape[0], -1)).tolist(),
            "variables": {k: v["data"] for k, v in d_["coords"].items()},
        }
        return d

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

    # just for asymmetric purposes, i.e., the NA outcome
    # symbolizing the asymmetry; otherwise, if outcome data
    # has changed, just remake the cpt
    def add_na_outcomes(self):
        raise NotImplementedError

    def to_pyagrum(self):
        variables = self.variables
        if len(variables) != 1:
            raise AgrumConversionError
        return [
            (
                {},
                [self._cpt.sel(**{variables[0]: state}) for state in self.outcomes],
            )
        ]

    def to_pycid(self):
        raise NotImplementedError
