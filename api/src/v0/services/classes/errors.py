"""
Error for services.classes errors
"""

import logging

logger = logging.getLogger(__name__)


class ProbabilityTypeError(Exception):
    def __init__(self, arg):
        error_message = f"Unreckonized probability type: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class DiscreteConditionalProbabilityTypeError(Exception):
    def __init__(self, arg):
        error_message = (
            f"Data cannot be used to create a DiscreteConditionalProbability: {arg}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class DiscreteUnconditionalProbabilityTypeError(Exception):
    def __init__(self, arg):
        error_message = (
            f"Data cannot be used to create a DiscreteUnconditionalProbability: {arg}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class DecisionNodeTypeError(Exception):
    def __init__(self, arg):
        error_message = f"Data cannot be used to create a DecisionNode: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class UncertaintyNodeTypeError(Exception):
    def __init__(self, arg):
        error_message = f"Data cannot be used to create a UncertaintyNode: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class UtilityNodeTypeError(Exception):
    def __init__(self, arg):
        error_message = f"Data cannot be used to create a UtilityNode: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class InfluenceDiagramNodeTypeError(Exception):
    def __init__(self, arg):
        error_message = f"Data cannot be used to create an influence diagram Node: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class NodeTypeError(Exception):
    def __init__(self, arg):
        error_message = f"Data is not an InfluenceDiagram Node: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class DescriptionValidationError(Exception):
    def __init__(self, arg):
        error_message = f"Input description is not a string: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class NameValidationError(Exception):
    def __init__(self, arg):
        error_message = f"Input name is not a string: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class ShortnameValidationError(Exception):
    def __init__(self, arg):
        error_message = f"Input shortname is not a string: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class UUIDValidationError(Exception):
    def __init__(self, arg):
        error_message = f"Input uuid is neither a valid uuid (version 4) nor None: {arg}"
        super().__init__(error_message)
        logger.critical(error_message)


class AlternativeValidationError(Exception):
    def __init__(self, arg):
        error_message = (
            f"Input alternatives is neither a list or "
            f"tuple of unique strings nor None: {arg}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class DiscreteProbabilityVariableValidationError(Exception):
    def __init__(self, arg):
        error_message = (
            f"One of the variables is not a dictionary with "
            f"element being able to be interpreted as 1D: {arg}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class DiscreteConditionalProbabilityFunctionValidationError(Exception):
    def __init__(self, arg):
        error_message = (
            f"The conditional probability function is not well formed size "
            f"(not compatible with variables or content is not normalized): {arg}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class DiscreteUnconditionalProbabilityFunctionValidationError(Exception):
    def __init__(self, arg):
        error_message = (
            f"The unconditional probability function is not well formed size "
            f"(not compatible with variables or content is not normalized): {arg}"
        )
        super().__init__(error_message)
        logger.critical(error_message)


class ProbabilityValidationError(Exception):
    def __init__(self, arg):
        error_message = (
            f"Input probability is neither a well formed probability nor None: {arg}"
        )
        super().__init__(error_message)
        logger.critical(error_message)
