import math
from typing import Literal

import numpy as np
from pydantic import (
    AliasChoices,
    ConfigDict,
    Field,
    constr,
    field_validator,
    model_validator,
)

from ... import DOTModel
from .meta import VertexMetaDataResponse


def none_probability_function(
        variables: dict[str, list[str]]
        ) -> list[list[None]]:
    """Create a list of list of None's
    
        This function is used to reset a probability function to None
        given the variables (with outcomes)

    Args:
        variables (dict): Representation of probability variables.
        They are a list of dictionaries, each as
        ```
        {'first': ['state1', 'state2'], 'second': ['out1', 'out2', 'out3']}
        ```

    Returns:
        list[list[None]]: The representation of a non-set probability
        function. The size of the output is given by the input variables.
        The size of axis 0 is preserved, the rest is flattened.
    """
    array_size = tuple([len(v) for v in variables.values()])
    probability_function = np.reshape(
        np.full(array_size, None), (array_size[0], -1)
        ).tolist()
    return probability_function    


def variables_probability_function_consistence(
        variables: dict,
        probability_function: list[list[float | None]]
        ) -> bool:
    """Check the consistence between the variables and the function of a probability

    Args:
        variables (dict): Variables of probability
        probability_function (list[list[float  |  None]]): Probability function

    Returns:
        bool: True if inputs are consistent, False otherwise
    """
    variables_values = list(variables.values())
    variables_size = [len(variables_values[0])]
    if len(variables_values) > 1:
        variables_size.append(math.prod([len(v) for v in variables_values[1:]]))
    else:
        variables_size.append(1)
    variables_size = tuple(variables_size)
    probability_function_size = np.asarray(probability_function).shape
    return variables_size == probability_function_size


def validate_uncertainty(value: dict):
    if value.get("category", None) != "Uncertainty":
        return value
    if value.get("uncertainty", None) is None:
        value["uncertainty"] = {
            "probability": None,
            "key": "False",
            "source": ""
        }
    if value["uncertainty"].get("probability", None) is not None:
        return value
    value["uncertainty"]["probability"] = default_probability(value)
    return value    


def validate_decision(value: dict):
    if value.get("category", None) != "Decision":
        return value
    if value.get("decision", None) is not None:
        return value
    value["decision"] = DecisionData()
    return value


def validate_value_metric(value: dict):
    if value.get("category", None) != "Value Metric":
        return value
    if value.get("value_metric", None) is not None:
        return value
    value["value_metric"] = ValueMetricData()
    return value


class DiscreteUnconditionalProbabilityData(DOTModel):
    """Model for the discrete unconditional probability description"""

    dtype: Literal["DiscreteUnconditionalProbability"]
    """Type of probability (Discrete unconditional)"""
    probability_function: list[list[float | None]]
    """Values of the probability itself"""
    variables: dict[str, list[str]]
    """variables and their outcomes"""    

    _previous: dict[str, list[str]] = None

    @model_validator(mode="after")
    def reset_probability_function(self):
        variables = self.variables
        probability_function = self.probability_function
        previous = self._previous
        if variables != self._previous:
            self._previous = variables
            if previous is not None:
                self.probability_function = none_probability_function(variables)
        if not variables_probability_function_consistence(variables, probability_function):
            self.probability_function = none_probability_function(variables)
        return self

        
class DiscreteConditionalProbabilityData(DOTModel):
    """Model for the discrete conditional probability description"""

    dtype: Literal["DiscreteConditionalProbability"]
    """Type of probability (Discrete conditional)"""
    probability_function: list[list[float]] | list[list[None]]
    """Values of the probability itself"""
    parents_uuid: list[str] | None = None
    """Sorted UUID's of parents for conditional proabilities"""
    conditioned_variables: dict[str, list[str]]
    """conditioned variables and their outcomes"""    
    conditioning_variables: dict[str, list[str]]
    """conditioning variables and their outcomes"""    

    _previous_conditioned: dict[str, list[str]] = None
    _previous_conditioning: dict[str, list[str]] = None

    @model_validator(mode="after")
    def reset_probability_function(self):
        conditioned_variables = self.conditioned_variables 
        conditioning_variables = self.conditioning_variables 
        variables = {**conditioned_variables, **conditioning_variables}

        probability_function = self.probability_function

        previous_conditioned = self._previous_conditioned
        previous_conditioning = self._previous_conditioning
        changes = False
        if previous_conditioned != self._previous_conditioned:
            self._previous_conditioned = previous_conditioned
            changes = True
        if previous_conditioning != self._previous_conditioning:
            self._previous_conditioning = previous_conditioning
            changes = True        
        if changes:
            if previous_conditioned is not None or previous_conditioning is not None:
                self.probability_function = none_probability_function(variables)
        if not variables_probability_function_consistence(variables, probability_function):
            self.probability_function = none_probability_function(variables)
        return self


def default_probability(data:dict) -> DiscreteUnconditionalProbabilityData:
    """Create an empty discrete unconditional probability

    Args:
        data (dict): data describing the issue

    Returns:
        DiscreteUnconditionalProbabilityData: a 1D discrete unconditional probability
        with only one outcome. The value of the probability is None
    """
    if data.get('shortname', None) is None:
        variable_name = 'variable'
    else:
        variable_name = data.get('shortname')
    outcomes = ['state1']
    variable = {variable_name: outcomes}
    pdf = none_probability_function(variable)
    return DiscreteUnconditionalProbabilityData(
        dtype="DiscreteUnconditionalProbability",
        probability_function=pdf,
        variables=variable
        )


class UncertaintyData(DOTModel):
    """Model gathering information about uncertainty"""
    
    probability: DiscreteUnconditionalProbabilityData | \
        DiscreteConditionalProbabilityData | \
              None  = Field(discriminator="dtype", default=None)
    """Probability data"""
    key: Literal["True", "False"] | None = None
    """Is the uncertainty a key uncertainty or not"""
    source: str = ""
    """Source of uncertainty information (subjective, data driven, literature...)"""

    @field_validator('probability', mode="before")
    def handle_none_case(cls, v):
        if v is None:
            return None
        return v

class DecisionData(DOTModel):
    """Model gathering information about decision"""

    states: list[str] | None = None
    """Possible alternatives (states) to the decision"""
    decision_type: Literal["Focus", "Tactical", "Strategic"] | None = None
    """Type of decision ("Focus", "Tactical", "Strategic")"""


class ValueMetricData(DOTModel):
    """Model gathering information about value metric"""

    cost_function: Literal["minimize_expected_utility", "maximize_expected_utility"] | None = None
    """Type of cost function for the value metric"""
    weigth: float | None = None 
    """Weight of the value metric for the global decision"""


class CommentData(DOTModel):
    """Model for comments on issues"""

    comment: str
    """Comment itself"""
    author: str
    """Author of the comment"""
    # date: datetime = Field(default_factory=lambda: datetime.now())


class IssueCreate(DOTModel):
    """Issue data model"""

    description: str
    """Description of the issue"""
    shortname: str | None = None
    (
        """Name of the issue. It should be given for at least all issues which will """
        """appear in the influence diagram and should be short as it will be """
        """displayed there"""
    )
    category: str | None = None
    """Category of the issue (Fact, Action Item, Decision, Uncertainty, Value Metric)"""
    tag: list[str] | None = None
    """List of user input keywords"""
    uncertainty: UncertaintyData | None = None
    """In case the issue is an uncertainty, Uncertainty information"""
    decision: DecisionData | None = None
    """In case the issue is a decision, Decision information"""
    value_metric: ValueMetricData | None = None
    """In case the issue is a value metric, Value Metric information"""
    boundary: Literal["in", "on", "out"] | None = None
    """Boundary of the issue (in, on, or out)"""
    comments: list[CommentData] | None = None
    """List of comments added to the issue"""
    index: str | None = None  # TODO: automatic assignment of index through API?
    """Index of the opportunity"""
    
    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "description": "this is an issue to call yours",
                    "shortname": "thelitissue",
                    "category": "Decision",
                    "tag": ["subsurface"],
                    "uncertainty": {
                        "probability": {
                            "dtype": "DiscreteUnconditionalProbability",
                            "probability_function": [[0.3], [0.7]],
                            "variables": {'variable': ['s1', 's2']}
                            },
                        "key": "True",
                        "source": "database analysis"
                        },
                    "decision": {
                            "states": ["yes", "no"],
                            "decision_type": "Focus"
                    },
                    "value_metric": {
                        "cost_function": "maximize_expected_utility",
                        "weigth": 1.0
                        },
                    "boundary": "in",
                    "comments": {
                        "comment": "Question: is this correct?",
                        "author": "John Doe",
                    },
                    "index": "0",
                }
            ]
        }
    )

    @model_validator(mode='before')
    @classmethod
    def set_default_probability(cls, value: dict):
        return validate_uncertainty(value)

    @model_validator(mode='before')
    @classmethod
    def set_default_decision(cls, value: dict):
        return validate_decision(value)

    @model_validator(mode='before')
    @classmethod
    def set_default_value_metric(cls, value: dict):
        return validate_value_metric(value)
            

class IssueUpdate(DOTModel):
    shortname: str | None = None
    description: str | None = None
    tag: list[str] | None = None
    category: str | None = None
    uncertainty: UncertaintyData | None = None
    decision: DecisionData | None = None
    value_metric: ValueMetricData | None = None
    boundary: Literal["in", "on", "out"] | None = None
    comments: list[CommentData] | None = None
    index: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "description": "this is an issue to call yours",
                    "shortname": "thelitissue",
                    "category": "Decision",
                    "tag": ["subsurface"],
                    "uncertainty": {
                        "probability": {
                            "dtype": "DiscreteUnconditionalProbability",
                            "probability_function": [[0.3], [0.7]],
                            "variables": {'variable': ['s1', 's2']}
                            },
                        "key": "True",
                        "source": "database analysis"
                        },
                    "decision": {
                            "states": ["yes", "no"],
                            "decision_type": "Focus"
                    },
                    "value_metric": {
                        "cost_function": "maximize_expected_utility",
                        "weigth": 1.0
                        },
                    "boundary": "in",
                    "comments": {
                        "comment": "Question: is this correct?",
                        "author": "John Doe",
                    },
                    "index": "0",
                }
            ]
        }
    )

    @model_validator(mode='before')
    @classmethod
    def set_default_probability(cls, value: dict):
        return validate_uncertainty(value)

    @model_validator(mode='before')
    @classmethod
    def set_default_decision(cls, value: dict):
        return validate_decision(value)

    @model_validator(mode='before')
    @classmethod
    def set_default_value_metric(cls, value: dict):
        return validate_value_metric(value)


class IssueResponse(VertexMetaDataResponse):
    shortname: str | None
    description: str
    tag: list[str] | None
    category: str | None
    uncertainty: UncertaintyData | None
    decision: DecisionData | None
    value_metric: ValueMetricData | None
    boundary: Literal["in", "on", "out"] | None
    comments: list[CommentData] | None
    index: str | None

    id: str = Field(validation_alias=AliasChoices("T.id", "id"))
    label: constr(to_lower=True) = Field(
        validation_alias=AliasChoices("T.label", "label")
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "description": "this is an issue to call yours",
                    "shortname": "thelitissue",
                    "category": "Decision",
                    "tag": ["subsurface"],
                    "uncertainty": {
                        "dtype": "DiscreteUnconditionalProbability",
                        "probability_function": [[0.3], [0.7]],
                        "variables": {'variable': ['s1', 's2']}
                        },
                    "decision": {
                            "states": ["yes", "no"],
                            "decision_type": "Focus"
                    },
                    "value_metric": {
                        "cost_function": "maximize_expected_utility",
                        "weigth": 1.0
                        },
                    "boundary": "in",
                    "comments": {
                        "comment": "Question: is this correct?",
                        "author": "John Doe",
                    },
                    "index": "0",
                }
            ]
        }
    )
