"""
This module converts probaility related data between the database formats
and the service layer formats
"""
import numpy as np

from src.v0.services.classes.abstract_probability import ProbabilityABC
from src.v0.services.classes.discrete_conditional_probability import (
    DiscreteConditionalProbability,
)
from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)

from ..errors import (
    DiscreteConditionalProbabilityTypeError,
    DiscreteUnconditionalProbabilityTypeError,
    ProbabilityTypeError,
)
from .base import ConversionABC


class DiscreteConditionalProbabilityConversion(ConversionABC):
    def from_json(self, probability: dict) -> DiscreteConditionalProbability:
        if probability.get("dtype") != "DiscreteConditionalProbability":
            raise DiscreteConditionalProbabilityTypeError(probability.get("dtype"))
        array_size = tuple([len(v) for v in probability["variables"].values()])
        distribution = np.reshape(
            np.asarray(probability["probability_function"]), array_size
                )
        return DiscreteConditionalProbability(distribution, probability["variables"])

    def to_json(self, probability: DiscreteConditionalProbability) -> dict:
        array_size = (
            probability._cpt.data.shape[0],
            np.astype(np.prod(probability._cpt.data.shape[1:]), int)
            )
        distribution = np.reshape(probability._cpt.data, array_size).tolist()

        return {
            "dtype": "DiscreteConditionalProbability",
            "probability_function": distribution,
            "variables": {k:v.data.tolist() for k,v in probability._cpt.coords.items()},
            }


class DiscreteUnconditionalProbabilityConversion(ConversionABC):
    def from_json(self, probability: dict) -> DiscreteUnconditionalProbability:
        if probability.get("dtype") != "DiscreteUnconditionalProbability":
            raise DiscreteUnconditionalProbabilityTypeError(probability.get("dtype"))
        array_size = tuple([len(v) for v in probability["variables"].values()])
        distribution = np.reshape(
            np.asarray(probability["probability_function"]), array_size
            )
        return DiscreteUnconditionalProbability(distribution,  probability["variables"])

    def to_json(self, probability: DiscreteUnconditionalProbability) -> dict:
        array_size = (
            probability._cpt.data.shape[0],
            np.astype(np.prod(probability._cpt.data.shape[1:]), int)
            )
        distribution = np.reshape(probability._cpt.data, array_size).tolist()
        return {
            "dtype": "DiscreteUnconditionalProbability",
            "probability_function": distribution,
            "variables": {k:v.data.tolist() for k,v in probability._cpt.coords.items()},
            }


class ProbabilityConversion(ConversionABC):
    def from_json(self, probability: dict | None) -> ProbabilityABC:
        if probability is None:
            return None
        if not isinstance(probability, dict):
            raise ProbabilityTypeError(type(probability))
        if probability.get("dtype") == "DiscreteUnconditionalProbability":
            return DiscreteUnconditionalProbabilityConversion().from_json(probability)
        if probability.get("dtype") == "DiscreteConditionalProbability":
            return DiscreteConditionalProbabilityConversion().from_json(probability)
        raise ProbabilityTypeError(type(probability))

    def to_json(self, probability: ProbabilityABC | None) -> dict:
        if probability is None:
            return None
        if isinstance(probability, DiscreteUnconditionalProbability):
            return DiscreteUnconditionalProbabilityConversion().to_json(probability)
        if isinstance(probability, DiscreteConditionalProbability):
            return DiscreteConditionalProbabilityConversion().to_json(probability)
        raise ProbabilityTypeError(type(probability))
