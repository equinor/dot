import numpy as np
import xarray as xr
from numpy.typing import ArrayLike

from src.v0.services.classes.abstract_probability import ProbabilityABC

from .validations import validate_and_set_probability


class DiscreteConditionalProbability(ProbabilityABC):
    """DiscreteConditionalProbability"""

    def __init__(self, probability_function: ArrayLike, variables: dict) -> None:
        """
         Parameters
         -----------
         probability_function: ArrayLike
             gives the probability that a variable is equal to some value
         variables: dict
             involves the variable name and its values; values refers to the
             set of possible outcomes

        .. note:
            Future:

            conditioned_variables: dict
                involves the variable name and its values; values refers to the
                set of possible outcomes
            conditioning_variables: dict
                involves the variable name and its values; values refers to the
                set of possible outcomes

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
        variable_list = list(variables.keys())
        variable_values = list(variables.values())
        conditioned_variables = {variable_list[0]: variable_values[0]}
        conditioning_variables = {
            variable_list[k]: variable_values[k] for k in range(1, len(variable_list))
        }
        conditioned_variables = validate_and_set_probability.discrete_variables(
            conditioned_variables
        )
        conditioning_variables = validate_and_set_probability.discrete_variables(
            conditioning_variables
        )
        probability_function = (
            validate_and_set_probability.discrete_conditional_probability_function(
                probability_function, conditioned_variables, conditioning_variables
            )
        )
        self._cpt = xr.DataArray(
            probability_function,
            coords={**conditioned_variables, **conditioning_variables},
            attrs={
                "conditioned_variables": list(conditioned_variables.keys()),
                "conditioning_variables": list(conditioning_variables.keys()),
            },
        )

    @property
    def outcomes(self):
        variable_names = self.conditioned_variables
        if len(variable_names) == 1:
            return tuple(self._cpt.coords[variable_names[0]].data.tolist())
        # FUTURE IMPLEMENTATION
        # else:
        #     return tuple(
        #         product(
        #             *tuple(tuple(self._cpt.coords[vn].data.tolist()) \
        #                    for vn in variable_names)
        #             )
        #         )

    @property
    def variables(self):
        return self._cpt.dims

    @property
    def conditioned_variables(self):
        return tuple(
            item
            for item in self._cpt.dims
            if item in self._cpt.attrs["conditioned_variables"]
        )

    @property
    def conditioning_variables(self):
        return tuple(
            item
            for item in self._cpt.dims
            if item in self._cpt.attrs["conditioning_variables"]
        )

    @classmethod
    def initialize_nan(cls, conditioned_variables: dict, conditioning_variables: dict):
        data_shape = tuple(
            np.asarray(v).shape[0]
            for v in {**conditioned_variables, **conditioning_variables}.values()
        )
        data = np.full(data_shape, np.nan)
        return cls(
            probability_function=data,
            variables=conditioned_variables | conditioning_variables,
        )

    @classmethod
    def initialize_uniform(
        cls, conditioned_variables: dict, conditioning_variables: dict
    ):
        data_shape = tuple(
            np.asarray(v).shape[0]
            for v in {**conditioned_variables, **conditioning_variables}.values()
        )
        data = np.ones(data_shape) / data_shape[0]
        return cls(
            probability_function=data,
            variables=conditioned_variables | conditioning_variables,
        )

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
