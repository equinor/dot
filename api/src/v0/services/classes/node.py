"""Nodes classes

NodeABC is an abstract class with 3 concretizations:
- DecisionNode
- UncertaintyNode
- UtilityNode
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence

from .abstract_probability import ProbabilityABC
from .validations import validate_and_set_node


class NodeABC(ABC):
    """Abstract class of nodes"""

    def __init__(self, *, description: str, shortname: str, uuid=None):
        """instantiation of an (abstract) node

        Args:
            description (str): description of the node
            shortname (str): shortname of the node
            uuid (str, optional): uuid. Defaults to None.
            If None, the uuid is attributed at instantiation.

        Private attributes:
            _description (str): description of the node
            _shortname (str): shortname of the node
            _uuid (str, optional): uuid. Defaults to None.
            If None, the uuid is attributed at instantiation.
        """
        self._description = validate_and_set_node.description(description)
        self._shortname = validate_and_set_node.shortname(shortname)
        self._uuid = validate_and_set_node.uuid(uuid)

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

    @description.setter
    def description(self, value):
        self._description = validate_and_set_node.description(value)

    @shortname.setter
    def shortname(self, value):
        self._shortname = validate_and_set_node.shortname(value)

    @uuid.setter
    def uuid(self, value):
        self._uuid = validate_and_set_node.uuid(value)

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
    def states(self):  # pragma: no cover
        raise NotImplementedError

    def copy(self):
        """Copy of the node, associating a new uuid

        Returns:
            NodeABC: a copy of the node, with a new uuid
        """
        copied_node = type(self)(description=self.description, shortname=self.shortname)
        for attribute, value in self.__dict__.items():
            if attribute not in ["_description", "_shortname", "_uuid"]:
                setattr(copied_node, attribute, value)
        return copied_node


class DecisionNode(NodeABC):
    """Decision node class"""

    def __init__(
        self,
        *,
        description: str,
        shortname: str,
        uuid=None,
        alternatives: Sequence[str] = None,
    ):
        """Create an instance of a DecisionNode

        Args:
            description (str): description of the node
            shortname (str): shortname of the node
            unique_id (str, optional): uuid. Defaults to None.
            If None, the uuid is attributed at instantiation.
            alternatives (Sequence[str], optional): alternatives (states)
            of the decision. Defaults to None.

        Private attributes:
            _description (str): description of the node
            _shortname (str): shortname of the node
            _unique_id (str, optional): uuid. Defaults to None.
            If None, the uuid is attributed at instantiation.
            _alternatives (Sequence[str], optional): alternatives (states) of
            the decision. Defaults to None.
        """
        super().__init__(description=description, shortname=shortname, uuid=uuid)
        self._alternatives = validate_and_set_node.alternatives(alternatives)

    @property
    def alternatives(self) -> list[str]:
        """
        Returns:
            List[str]: the alternatives (states) of the decision
        """
        if isinstance(self._alternatives, list):
            return self._alternatives
        if isinstance(self._alternatives, Sequence):
            return list(self._alternatives)
        return []

    @alternatives.setter
    def alternatives(self, value):
        self._alternatives = validate_and_set_node.alternatives(value)

    @property
    def states(self) -> list[str]:
        """
        Returns:
            List[str]: the alternatives (states) of the decision
        """
        return self.alternatives


class UncertaintyNode(NodeABC):
    """Uncertainty (or chance) node class"""

    def __init__(
        self,
        *,
        description: str,
        shortname: str,
        uuid=None,
        probability: ProbabilityABC = None,
    ):
        """Create an instance of a UncertaintyNode

        Args:
            description (str): description of the node
            shortname (str): shortname of the node
            unique_id (str, optional): uuid. Defaults to None.
            If None, the uuid is attributed at instantiation.
            probability (ProbabilityABC, optional): probability associated to the node.
            Defaults to None.

        Private attributes:
            _description (str): description of the node
            _shortname (str): shortname of the node
            _unique_id (str, optional): uuid. Defaults to None.
            If None, the uuid is attributed at instantiation.
            _probability (ProbabilityABC, optional): probability associated to the node.
            Defaults to None.
        """
        super().__init__(description=description, shortname=shortname, uuid=uuid)
        self._probability = validate_and_set_node.probability(probability)

    @property
    def probability(self) -> ProbabilityABC:
        """
        Returns:
            ProbabilityABC: the probabibility associated to the node
        """
        return self._probability

    @probability.setter
    def probability(self, value):
        self._probability = validate_and_set_node.probability(value)

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
        if self.probability is None:
            return ()
        return self._probability.outcomes


class UtilityNode(NodeABC):
    """Utility (or value) node class"""

    def __init__(self, *, description: str, shortname: str, uuid=None):
        """Create an instance of a UtilityNode

        Args:
            description (str): description of the node
            shortname (str): shortname of the node
            unique_id (str, optional): uuid. Defaults to None.
            If None, the uuid is attributed at instantiation.

        Private attributes:
            _description (str): description of the node
            _shortname (str): shortname of the node
            _unique_id (str, optional): uuid. Defaults to None.
            If None, the uuid is attributed at instantiation.

        TODO: implement utility matrix attribute through a Utility class.
        So far it is rather a place holder.
        TODO: implement the value metric in addition to the consequence
        TODO: the total objective is a combination of gains and costs of each
        decision and how we combine them into a desired objective
        """
        super().__init__(description=description, shortname=shortname, uuid=uuid)

    @property
    def states(self) -> list[str]:
        """
        Returns:
            List[str]: the consequence entries (states) of the utility
        """
        pass
