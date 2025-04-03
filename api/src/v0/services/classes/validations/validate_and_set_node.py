
from collections.abc import Sequence
from typing import Any
from uuid import UUID, uuid4

from src.v0.services.classes.abstract_probability import ProbabilityABC
from src.v0.services.classes.discrete_conditional_probability import (
    DiscreteConditionalProbability,
)
from src.v0.services.classes.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)
from src.v0.services.classes.errors import (
    AlternativeValidationError,
    DescriptionValidationError,
    NameValidationError,
    ProbabilityValidationError,
    ShortnameValidationError,
    UUIDValidationError,
)


def description(arg: Any) -> str:
    if not isinstance(arg, str):
        raise DescriptionValidationError(arg)
    return arg


def name(arg: Any) -> str:
    if not isinstance(arg, str):
        raise NameValidationError(arg)
    return arg


def shortname(arg: Any) -> str:
    if not isinstance(arg, str):
        raise ShortnameValidationError(arg)
    return arg


def uuid(arg: Any) -> str:
    if not (isinstance(arg, (str, UUID)) or arg is None):
        raise UUIDValidationError(arg)
    if arg is None:
        return str(uuid4())
    if isinstance(arg, UUID) and arg.version == 4:
        return str(arg)
    try:  # if arg is str
        assert UUID(arg).version == 4
        return arg
    except:
        raise UUIDValidationError(arg)


def alternatives(arg: Any) -> Sequence | None:
    if isinstance(arg, str):
        raise AlternativeValidationError(arg)
    if not (isinstance(arg, Sequence) or arg is None):
        raise AlternativeValidationError(arg)
    if arg is None:
        return arg
    if not all([isinstance(item, str) for item in arg]):
        raise AlternativeValidationError(arg)
    if len(arg) != len(set(arg)):
        raise AlternativeValidationError(arg)
    return arg


def probability(arg: Any) -> ProbabilityABC:
    if not (
        isinstance(arg, DiscreteConditionalProbability)
        or isinstance(arg, DiscreteUnconditionalProbability)
        or arg is None
    ):
        raise ProbabilityValidationError(arg)
    return arg
