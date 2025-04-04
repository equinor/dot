"""
This module converts issue related data between the database formats
and the service layer formats
"""

from collections.abc import Sequence

from src.v0.services.classes.node import (
    DecisionNode,
    NodeABC,
    UncertaintyNode,
    UtilityNode,
)

from ..errors import (
    DecisionNodeTypeError,
    InfluenceDiagramNodeTypeError,
    NodeTypeError,
    UncertaintyNodeTypeError,
    UtilityNodeTypeError,
)
from .base import ConversionABC, MetadataCreate
from .probability import ProbabilityConversion


def add_metadata(uuid: str) -> dict:
    metadata = MetadataCreate.vertex(uuid)
    return {
        "uuid": metadata.uuid,
        "timestamp": metadata.timestamp,
        "date": metadata.date,
        "id": metadata.uuid,
        "label": "issue",
    }


class DecisionJSONConversion:
    """
    Conversion to json of fields relevant for decision
    """

    def states(self, node):
        return (
            None
            if (isinstance(node.alternatives, Sequence) and len(node.alternatives) == 0)
            else node.alternatives
        )

    def decision_type(self, node):
        return "Focus"


class UncertaintyJSONConversion:
    """
    Conversion to json of fields relevant for uncertainty
    """

    def probability(self, node):
        return (
            None
            if (node.probability is None)
            else ProbabilityConversion().to_json(node.probability)
        )

    def key_uncertainty(self, node):
        return "true"

    def source(self, node):
        return ""


class DecisionNodeConversion(ConversionABC):
    """
    Concrete implementation of `from_json` and `to_json` for decisions.
    """

    def from_json(self, issue: dict) -> DecisionNode:
        if issue.get("category") != "Decision":
            raise DecisionNodeTypeError(issue.get("category"))
        return DecisionNode(
            description=issue.get("description"),
            shortname=issue.get("shortname"),
            uuid=issue.get("uuid"),
            alternatives=issue.get("alternatives"),
        )

    def to_json(self, node: DecisionNode) -> dict:
        data = {
            "category": "Decision",
            "shortname": node.shortname,
            "description": node.description,
            "alternatives": DecisionJSONConversion().states(node),
            "decisionType": DecisionJSONConversion().decision_type(node),
            "boundary": "in",
        }
        return data | add_metadata(node.uuid)


class UncertaintyNodeConversion(ConversionABC):
    """
    Concrete implementation of `from_json` and `to_json` for uncertainties.
    """

    def from_json(self, issue: dict) -> UncertaintyNode:
        if issue.get("category") != "Uncertainty":
            raise UncertaintyNodeTypeError(issue.get("category"))
        try:
            probability = ProbabilityConversion().from_json(issue.get("probabilities"))
        except Exception as e:
            raise UncertaintyNodeTypeError(e)
        return UncertaintyNode(
            description=issue.get("description"),
            shortname=issue.get("shortname"),
            uuid=issue.get("uuid"),
            probability=probability,
        )

    def to_json(self, node: UncertaintyNode) -> dict:
        try:
            probability = ProbabilityConversion().to_json(node.probability)
        except Exception as e:
            raise UncertaintyNodeTypeError(e)
        data = {
            "category": "Uncertainty",
            "shortname": node.shortname,
            "description": node.description,
            "probabilities": probability,
            "keyUncertainty": "true",
            "boundary": "in",
        }
        return data | add_metadata(node.uuid)


class UtilityNodeConversion(ConversionABC):
    """
    Concrete implementation of `from_json` and `to_json` for utilities.

    .. warning:
        In this implementation we assume Utility is Value Metric which is not the
        case and will be modified in future version
    """

    def from_json(self, issue: dict) -> UtilityNode:
        if issue.get("category") != "Value Metric":
            raise UtilityNodeTypeError(issue.get("category"))
        return UtilityNode(
            description=issue.get("description"),
            shortname=issue.get("shortname"),
            uuid=issue.get("uuid"),
        )

    def to_json(self, node: UtilityNode) -> dict:
        data = {
            "category": "Value Metric",
            "shortname": node.shortname,
            "description": node.description,
            "boundary": "in",
        }
        return data | add_metadata(node.uuid)


class InfluenceDiagramNodeConversion(ConversionABC):
    def from_json(self, issue: dict) -> NodeABC:
        """Create a node from a json stream.

        Only key uncertainties, focus decisions and utilities are converted.

        Args:
            issue (Dict): issue as a dictionary

        Raises:
            InfluenceDiagramTypeError: _description_

        Returns:
            NodeABC: The converted node.
        """
        if issue.get("category") not in ["Decision", "Uncertainty", "Value Metric"]:
            raise InfluenceDiagramNodeTypeError(f'category: {issue.get("category")}')
        if issue.get("boundary") not in ["in", "on"]:
            raise InfluenceDiagramNodeTypeError(f'boundary: {issue.get("boundary")}')
        if not issue.get("shortname"):
            raise InfluenceDiagramNodeTypeError(f'shortname: {issue.get("shortname")}')
        if issue["category"] == "Decision":
            if issue.get("decisionType") != "Focus":
                raise InfluenceDiagramNodeTypeError(
                    f'decisionType: {issue.get("decisionType")}'
                )
            return DecisionNodeConversion().from_json(issue)
        if issue["category"] == "Uncertainty":
            if issue["keyUncertainty"] != "true":
                raise InfluenceDiagramNodeTypeError(
                    f'keyUncertainty: {issue.get("keyUncertainty")}'
                )
            return UncertaintyNodeConversion().from_json(issue)
        if issue["category"] == "Value Metric":
            return UtilityNodeConversion().from_json(issue)

    def to_json(self, node: NodeABC) -> dict:
        if isinstance(node, DecisionNode):
            return DecisionNodeConversion().to_json(node)
        if isinstance(node, UncertaintyNode):
            return UncertaintyNodeConversion().to_json(node)
        if isinstance(node, UtilityNode):
            return UtilityNodeConversion().to_json(node)
        raise NodeTypeError(node)
