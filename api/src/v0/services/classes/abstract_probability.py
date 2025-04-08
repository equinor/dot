import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ProbabilityABC(ABC):
    """ProbabilityABC"""

    @classmethod
    @abstractmethod
    def initialize_nan(cls, *args, **kwargs):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def initialize_uniform(cls, *args, **kwargs):
        raise NotImplementedError

    @property
    @abstractmethod
    def variables(self):
        raise NotImplementedError

    @abstractmethod
    def get_distribution(self, **kwargs):
        raise NotImplementedError
