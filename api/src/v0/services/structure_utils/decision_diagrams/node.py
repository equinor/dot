"""Nodes classes

NodeABC is an abstract class with 3 concretizations:
- DecisionNode
- UncertaintyNode
- UtilityNode

    Raises:
        NodeTypeError: When failing to create an instance of a node
"""

from __future__ import annotations

import ast
import logging
import re
from abc import ABC, abstractmethod
from importlib import import_module
from typing import TYPE_CHECKING
from uuid import uuid4

from ..probability.discrete_conditional_probability import DiscreteConditionalProbability
from ..probability.discrete_unconditional_probability import (
    DiscreteUnconditionalProbability,
)

if TYPE_CHECKING:  # pragma: no cover
    from ....models.issue import IssueResponse
    from ..probability.abstract_probability import ProbabilityABC


logger = logging.getLogger(__name__)


class NodeTypeError(Exception):
    def __init__(self, node_type):
        error_message = f"failing instantiation of {node_type}"
        super().__init__(error_message)
        logger.critical(error_message)


class NodeABC(ABC):
    """Abstract class of nodes"""

    def __init__(self, shortname: str, description: str, unique_id=None):
        """instantiation of an (abstract) node

        Args:
            description (str): description of the node
            shortname (str): shortname of the node
            unique_id (str, optional): uuid. Defaults to None. If None, the uuid is
                                       attributed at instantiation.

        Private attributes:
            _description (str): description of the node
            _shortname (str): shortname of the node
            _unique_id (str, optional): uuid. Defaults to None. If None, the uuid is
                                        attributed at instantiation.
        """
        self._shortname = shortname
        self._description = description
        self._uuid = unique_id if unique_id is not None else str(uuid4())

    @property
    def description(self) -> str:
        """Return the `description` attribute

        Returns:
            str: description of the node
        """
        return self._description

    @property
    def shortname(self) -> str:
        """Return the `shortname` attribute

        Returns:
            str: shortname of the node
        """
        return self._shortname

    @property
    def uuid(self) -> str:
        """Return the `uuid` attribute

        Returns:
            str: uuid of the node
        """
        return self._uuid

    @property
    def is_decision_node(self) -> bool:
        """
        Returns:
            bool: True of the node is a DecisionNode, false otherwise
        """
        return isinstance(self, DecisionNode)

    @property
    def is_uncertainty_node(self) -> bool:
        """
        Returns:
            bool: True of the node is a UncertaintyNode, false otherwise
        """
        return isinstance(self, UncertaintyNode)

    @property
    def is_utility_node(self) -> bool:
        """
        Returns:
            bool: True of the node is a UtilityNode, false otherwise
        """
        return isinstance(self, UtilityNode)

    @property
    @abstractmethod
    def states(self):
        raise NotImplementedError

    def copy(self):
        """Copy of the node

        Returns:
            NodeABC: a copy of the node, with a new uuid
        """
        shortname = self.shortname
        description = self.description
        copied_node = type(self)(shortname, description)
        for attribute, value in self.__dict__.items():
            if attribute not in ["_shortname", "_description", "_uuid"]:
                setattr(copied_node, attribute, value)
        return copied_node

    def to_dict(self) -> dict:
        """Convert the Node object into a dictionary

        Each property becomes the key of a dictionary.
        Private and restricted attributes loose their underscores

        Returns:
            Dict: a dictionary representing the node
        """
        d = {"node_type": self.__class__.__name__}
        properties = self.__dict__
        for property in properties:
            key = property.lstrip("_")
            if hasattr(getattr(self, key, None), "to_dict"):
                d[key] = getattr(self, key).to_dict()
            else:
                d[key] = getattr(self, key, None)
        return d

    @staticmethod
    @abstractmethod
    def get_instance_input(issue):
        raise NotImplementedError

    @staticmethod
    def from_dict(data: dict) -> NodeABC:
        """Create a Node from data in a dictionary

        Args
            data (Dict): dictionary describing the node
                keys are:
                'node_type': the name of the Node instance as a string
                relevant keys according to the type of node

        Returns
            NodeABC: the created concrete type of Node

        Example:
            >>> node = {
            ...     'node_type': 'DecisionNode',
            ...     'description': "a decision",
            ...     'shortname': "D"
            ...        }
            >>> Node.from_dict(node)
        """
        node_type = data.pop("node_type")
        try:
            node = globals()[node_type](**data)
        except Exception:
            raise NodeTypeError(node_type)
        return node

    @staticmethod
    def from_db(response: IssueResponse) -> NodeABC:
        """Create a node from DataBase data

        Args:
            response (IssueResponse): response describing the node
                attributes are:
                'category': the name of the Node instance as a string
                relevant attributes according to the type of node

        Returns
            NodeABC: the created concrete type of Node
        """
        node_type = response.category
        node_type = "Utility" if node_type == "Value Metric" else node_type
        node_type += "Node"
        try:
            issue_data = globals()[node_type].get_instance_input(response)
        except Exception:
            raise NodeTypeError(node_type)

        issue_data_parsed = {}
        for k, v in issue_data.items():
            try:
                v = ast.literal_eval(v)
            except Exception as exc:
                e = exc
            finally:
                if e:
                    pass  # trick for passing ruff and bandit...
                issue_data_parsed[k] = v
        node = globals()[node_type]._from_db_model(**issue_data_parsed)
        return node

    @classmethod
    @abstractmethod
    def _from_db_model(cls, **kwargs):
        raise NotImplementedError


class DecisionNode(NodeABC):
    """Decision node class"""

    def __init__(
        self,
        shortname: str,
        description: str,
        uuid=None,
        alternatives=None,
        **kwargs,
    ):
        """Create an instance of a DecisionNode

        Args:
            description (str): description of the node
            shortname (str): shortname of the node
            unique_id (str, optional): uuid. Defaults to None. If None, the uuid is
                                       attributed at instantiation.
            alternatives (List[str], optional): alternatives (states) of the decision.
                                                Defaults to None.

        Private attributes:
            _description (str): description of the node
            _shortname (str): shortname of the node
            _unique_id (str, optional): uuid. Defaults to None. If None, the uuid is
                                        attributed at instantiation.
            _alternatives (List[str], optional): alternatives (states) of the decision.
                                                 Defaults to None.
        """
        super().__init__(shortname, description, uuid)
        self._alternatives = alternatives

    @staticmethod
    def get_instance_input(issue: IssueResponse) -> dict:
        """Get the relevant input for the instantiation

        Args:
            issue (IssueResponse): issue from the DataBase

        Returns:
            Dict: keys/values of the DataBase issue relevant for the instantiation
        """
        input_list = ["description", "shortname", "uuid", "alternatives"]
        return {key: getattr(issue, key) for key in input_list}

    @property
    def states(self) -> list[str]:
        """
        Returns:
            List[str]: the alternatives (states) of the decision
        """
        return self.alternatives

    @property
    def alternatives(self) -> list[str]:
        """
        Returns:
            List[str]: the alternatives (states) of the decision
        """
        return self._alternatives if isinstance(self._alternatives, list) else []

    @classmethod
    def _from_db_model(cls, **kwargs):
        """instantiation from the DataBase Model

        Args:
            kwargs: keys/values of the DataBase issue relevant for the instantiation
        """
        return cls(**kwargs)


class UncertaintyNode(NodeABC):
    """Uncertainty (or chance) node class"""

    def __init__(
        self,
        shortname: str,
        description: str,
        uuid=None,
        probabilities: ProbabilityABC = None,
        **kwargs,
    ):
        """Create an instance of a UncertaintyNode

        Args:
            description (str): description of the node
            shortname (str): shortname of the node
            unique_id (str, optional): uuid. Defaults to None. If None, the uuid is
                                       attributed at instantiation.
            probabilities (ProbabilityABC, optional): probability associated to the node.
                                                      Defaults to None.

        Private attributes:
            _description (str): description of the node
            _shortname (str): shortname of the node
            _unique_id (str, optional): uuid. Defaults to None. If None, the uuid is
                                        attributed at instantiation.
            _probabilities (ProbabilityABC, optional): probability associated to the
                                                       node. Defaults to None.
        """
        super().__init__(shortname, description, uuid)
        self._probabilities = probabilities

    @staticmethod
    def get_instance_input(issue: IssueResponse) -> dict:
        """Get the relevant input for the instantiation

        Args:
            issue (IssueResponse): issue from the DataBase

        Returns:
            Dict: keys/values of the DataBase issue relevant for the instantiation
        """
        input_list = ["description", "shortname", "uuid", "probabilities"]
        return {key: getattr(issue, key) for key in input_list}

    @property
    def probabilities(self) -> ProbabilityABC:
        """
        Returns:
            ProbabilityABC: the probabibility associated to the node
        """
        return self._probabilities

    @property
    def states(self) -> list[str]:
        """
        Returns:
            List[str]: the outcomes (states) of the uncertainty
        """
        return self.outcomes

    @property
    def outcomes(self) -> list[str]:
        """
        Returns:
            List[str]: the outcomes (states) of the uncertainty
        """
        if not isinstance(
            self._probabilities, DiscreteConditionalProbability
        ) and not isinstance(self._probabilities, DiscreteUnconditionalProbability):
            return ()
        return self._probabilities.outcomes

    @classmethod
    def _from_db_model(cls, **kwargs):
        """instantiation from the DataBase Model

        Args:
            kwargs: keys/values of the DataBase issue relevant for the instantiation
        """
        if kwargs["probabilities"] is not None:
            ptype = kwargs["probabilities"].dtype
            module_name = (
                "src.v0.services.structure_utils.probability."
                + re.sub(r"([a-z](?=[A-Z])|[A-Z](?=[A-Z][a-z]))", r"\1 ", ptype)
                .replace(" ", "_")
                .lower()
            )
            kwargs["probabilities"] = getattr(
                import_module(module_name), ptype
            ).from_db_model(kwargs["probabilities"])
        return cls(**kwargs)


class UtilityNode(NodeABC):
    """Utility (or value) node class"""

    def __init__(
        self,
        shortname: str,
        description: str,
        uuid=None,
        utility=None,
        **kwargs,
    ):
        """Create an instance of a UtilityNode

        Args:
            description (str): description of the node
            shortname (str): shortname of the node
            unique_id (str, optional): uuid. Defaults to None. If None, the uuid is
                                             attributed at instantiation.
            utility (List[str], optional): utility associated to the node. Defaults to
                                           None.

        Private attributes:
            _description (str): description of the node
            _shortname (str): shortname of the node
            _unique_id (str, optional): uuid. Defaults to None. If None, the uuid is
                                        attributed at instantiation.
            _utility (List[str], optional): utility associated to the node. Defaults to
                                            None.

        TODO: implement utility matrix attribute through a Utility class. So far it is
              rather a place holder.
        """
        super().__init__(shortname, description, uuid)
        self._utility = utility  # The value is typically E[gain] but we could minimize
        # the risk instead of maximizing the gain

    @staticmethod
    def get_instance_input(issue: IssueResponse) -> dict:
        """Get the relevant input for the instantiation

        Args:
            issue (IssueResponse): issue from the DataBase

        Returns:
            Dict: keys/values of the DataBase issue relevant for the instantiation
        """
        input_list = [
            "description",
            "shortname",
            "uuid",
        ]  # TODO: Add utility field to DB
        return {key: getattr(issue, key) for key in input_list}

    @property
    def states(self) -> list[str]:
        """
        Returns:
            List[str]: the utility entries (states) of the utility
        """
        return self.utility

    @property
    def utility(self) -> list[str]:
        """
        Returns:
            List[str]: the utility entries (states) of the utility
        """
        return self._utility if isinstance(self._utility, list) else []

    @classmethod
    def _from_db_model(cls, **kwargs):
        """instantiation from the DataBase Model

        Args:
            kwargs: keys/values of the DataBase issue relevant for the instantiation
        """
        return cls(**kwargs)
