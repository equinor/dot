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
        error_message = f"Expected DiscreteConditionalProbability dtype, got {cpt_type}"
        super().__init__(error_message)
        logger.critical(error_message)


class DiscreteConditionalProbability(ProbabilityABC):
    """DiscreteConditionalProbability"""

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

         For the Conditional Probability Table, P(Test Result | Test, State) such as

                        || 1. Test  ||    yes     yes   |  no      no
                        || 2. State ||   Peach | Lemon  | Peach | Lemon
        -----------------------------------------------------------------
         0. Test Result ||          ||         |        |       |
        -----------------------------------------------------------------
         no Test        ||          ||   0.1   |  0.05  |  0.85 |  0.46
         Peach          ||          ||   0.7   |  0.35  |  0.12 |  0.26
         Lemon          ||          ||   0.2   |  0.60  |  0.03 |  0.28

         the probability_function will be
             [
                 [0.1, 0.05, 0.85, 0.46],
                 [0.7, 0.35, 0.12, 0.26],
                 [0.2, 0.60, 0.03, 0.28],
             ]

         and the variables
             {
                 "Test Result": ["no Test", "Peach", "Lemon"],
                 "Test": ["yes", "no"],
                 "State": ["Peach", "Lemon"],
             }
        """
        super().__init__()
        if any(
            max(np.asarray(v).shape) != np.asarray(v).size for v in variables.values()
        ):
            raise VariableNot1D
        # remove white spaces as the string is used as variable name by xarray
        variables = {re.sub(r"\s+", "", k): v for k, v in variables.items()}
        self._cpt = xr.DataArray(probability_function, coords=variables)

    @property
    def outcomes(self):
        variable_name = self._cpt.dims[0]
        return tuple(self._cpt.coords[variable_name].data.tolist())

    @property
    def variables(self):
        return self._cpt.dims

    @classmethod
    def from_db_model(cls, data):
        array_size = tuple([len(v) for v in data.variables.values()])
        distribution = np.reshape(data.probability_function, array_size)
        return cls(distribution, data.variables)

    def add_conditioning_variable(self, variables: dict):
        raise NotImplementedError

    def remove_conditioning_variable(self, variables: dict):
        raise NotImplementedError

    @classmethod
    def initialize_nan(cls, variables: dict):
        data_shape = tuple(np.asarray(v).shape[0] for v in variables.values())
        return cls(np.full(data_shape, np.nan), variables=variables)

    def set_to_uniform(self):
        data_shape = tuple(np.asarray(v).shape[0] for v in self._cpt.coords.values())
        self._cpt.data = np.ones(data_shape) / data_shape[0]
        return self

    def normalize(self):
        self._cpt = self._cpt / np.apply_over_axes(
            np.sum, self._cpt, range(1, self._cpt.ndim)
        )
        return self

    def isnormalized(self, threshold=1e-6):
        return np.all(np.linalg.norm(self._cpt.sum(axis=0) - 1.0) < threshold)

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
        d = {
            "dtype": self.__class__.__name__,
            "probability_function": d_["data"],
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
        # agrum = list()
        coords = self._cpt.coords
        variables = {
            key: coords[key].data.tolist() for key in coords if key is not coords.dims[0]
        }
        agrum_dict = {k: list(range(len(v))) for k, v in variables.items()}
        agrum_dict = [
            dict(zip(agrum_dict.keys(), values, strict=False))
            for values in product(*agrum_dict.values())
        ]
        agrum_prob = [
            self.get_distribution(
                **{key: coords[key][val] for key, val in item.items()}
            ).data.tolist()
            for item in agrum_dict
        ]
        agrum = list(zip(agrum_dict, agrum_prob, strict=False))
        return agrum

    def to_pycid(self):
        raise NotImplementedError
