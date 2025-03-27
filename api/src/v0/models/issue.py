from typing import Literal

import numpy as np
from pydantic import (
    AliasChoices,
    ConfigDict,
    Field,
    constr,
    model_validator,
)

from ... import DOTModel
from .meta import VertexMetaDataResponse


class IssueValidator(DOTModel):
    @model_validator(mode="before")
    def set_shortname_as_probability_variable(cls, values):
        if values.get("probabilities", None) is None:
            variable_name = values.get("shortname", "variable")
            if not variable_name:
                variable_name = "variable"
            pdf = {
                "dtype": "DiscreteUnconditionalProbability",
                "probability_function": [[None]],
                "variables": {variable_name: ["outcome"]},
            }
            values["probabilities"] = ProbabilityData.model_validate(pdf)
        return values


class ProbabilityData(DOTModel):
    """Model for the probability description"""

    dtype: Literal["DiscreteUnconditionalProbability", "DiscreteConditionalProbability"]
    """Type of probability (Discrete conditional/unconditional)"""
    probability_function: list[list[float]] | list[list[None]]
    """Values of the probability itself"""
    variables: dict[str, list[str]]
    """variables and their outcomes"""

    @model_validator(mode="before")
    @classmethod
    def nullify_probability_function(cls, values):
        variables = values["variables"]
        array_size = tuple([len(v) for v in variables.values()])
        probability_function = values["probability_function"]
        if np.asarray(array_size).prod() != np.asarray(probability_function).size:
            probability_function = np.reshape(
                np.full(array_size, None), (array_size[0], -1)
            ).tolist()
        values["variables"] = variables
        values["probability_function"] = probability_function
        return values


class UncertaintyData(DOTModel):
    """Model gathering information about uncertainty"""

    probability: ProbabilityData | None = None
    """Probability data"""
    key: str = "False"
    """Is the uncertainty a key uncertainty or not"""
    source: str = ""
    """Source of uncertainty information (subjective, data driven, literature...)"""


class DecisionData(DOTModel):
    """Model gathering information about decision"""

    states: list[str] | None = None
    """Possible alternatives (states) to the decision"""
    decision_type: Literal["Focus", "Tactical", "Strategic"] | None = None
    """Type of decision ("Focus", "Tactical", "Strategic")"""


class ValueMetricData(DOTModel):
    """Model gathering information about value metric"""

    cost_function: Literal["minimize_expected_utility", "maximize_expected_utility"] = "maximize_expected_utility"
    """Type of cost function for the value metric"""
    weigth: float = 1.0
    """Weight of the value metric for the global decision"""


class CommentData(DOTModel):
    """Model for comments on issues"""

    comment: str
    """Comment itself"""
    author: str
    """Author of the comment"""
    # date: datetime = Field(default_factory=lambda: datetime.now())


class IssueCreate(IssueValidator):
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
    tag: list[str] | None = None
    """List of user input keywords"""
    """Category of the issue (Fact, Action Item, Decision, Uncertainty, Value Metric)"""
    keyUncertainty: str | None = None  # (True/False)
    (
        """In case the issue is an uncertainty, true if it """
        """is a key uncertainty, false otherwise"""
    )
    decisionType: str | None = None  # [Focus/Tactical/Strategic]
    """In case the issue is a decision, type of decision (Strategic, Focus, Tactical)"""
    probabilities: ProbabilityData | None = None  #  = default_probability  # None
    """In case the issue is an uncertainty, probability description"""
    alternatives: list[str] | None = None
    """In case the issue is a decision, list of alternatives"""
    boundary: Literal["in", "on", "out"] | None = None
    """Boundary of the issue (in, on, or out)"""
    comments: list[CommentData] | None = None
    """List of comments added to the issue"""
    uncertainty: UncertaintyData | None = None
    """In case the issue is an uncertainty, Uncertainty information"""
    decision: DecisionData | None = None
    """In case the issue is a decision, Decision information"""
    value_metric: ValueMetricData | None = None
    """In case the issue is a value metric, Value Metric information"""
    influenceNodeUUID: str | None = None
    """Deprecated"""
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
                    "keyUncertainty": "true",
                    "decisionType": "tactical",
                    "probabilities": {
                        "dtype": "DiscreteUnconditionalProbability",
                        "probability_function": [[0.5, 0.5], [0.4, 0.6]],
                        "variables": {
                            "Node1": ["Outcome1", "Outcome2"],
                            "Node2": ["Outcome21", "Outcome22"],
                        },
                    },
                    "alternatives": '["do or do not", "there is no try"]',
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


class IssueUpdate(IssueValidator):
    shortname: str | None = None
    description: str | None = None
    tag: list[str] | None = None
    category: str | None = None
    index: str | None = None
    keyUncertainty: str | None = None
    decisionType: str | None = None
    alternatives: list[str] | None = None
    probabilities: ProbabilityData | None = None
    influenceNodeUUID: str | None = None
    boundary: str | None = None
    comments: list[CommentData] | None = None
    uncertainty: UncertaintyData | None = None
    decision: DecisionData | None = None
    value_metric: ValueMetricData | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "shortname": "thelitissue",
                    "description": "this is an issue to call yours",
                    "tag": ["subsurface"],
                    "category": "Decision",
                    "index": "0",
                    "keyUncertainty": "true",
                    "decisionType": "tactical",
                    "alternatives": '["do or do not", "there is no try"]',
                    "probabilities": {
                        "dtype": "DiscreteUnconditionalProbability",
                        "probability_function": [[0.5, 0.5], [0.4, 0.6]],
                        "variables": {
                            "Node1": ["Outcome1", "Outcome2"],
                            "Node2": ["Outcome21", "Outcome22"],
                        },
                    },
                    "influenceNodeUUID": "123",
                    "boundary": "in",
                    "comments": {
                        "comment": "Question: is this correct?",
                        "author": "John Doe",
                    },
                }
            ]
        }
    )


class IssueResponse(VertexMetaDataResponse):
    shortname: str | None
    description: str
    tag: list[str] | None
    category: str | None
    index: str | None
    keyUncertainty: str | None
    decisionType: str | None
    alternatives: list[str] | None
    probabilities: ProbabilityData | None
    influenceNodeUUID: str | None
    boundary: str | None
    comments: list[CommentData] | None
    uncertainty: UncertaintyData | None = None
    decision: DecisionData | None = None
    value_metric: ValueMetricData | None = None

    id: str = Field(validation_alias=AliasChoices("T.id", "id"))
    label: constr(to_lower=True) = Field(
        validation_alias=AliasChoices("T.label", "label")
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "shortname": "thelitissue",
                    "description": "this is an issue to call yours",
                    "tag": ["subsurface"],
                    "category": "Decision",
                    "index": "0",
                    "keyUncertainty": "true",
                    "decisionType": "tactical",
                    "alternatives": '["do or do not", "there is no try"]',
                    "probabilities": {
                        "dtype": "DiscreteUnconditionalProbability",
                        "probability_function": [[0.5, 0.5], [0.4, 0.6]],
                        "variables": {
                            "Node1": ["Outcome1", "Outcome2"],
                            "Node2": ["Outcome21", "Outcome22"],
                        },
                    },
                    "influenceNodeUUID": "123",
                    "boundary": "in",
                    "comments": {
                        "comment": "Question: is this correct?",
                        "author": "John Doe",
                    },
                }
            ]
        }
    )
