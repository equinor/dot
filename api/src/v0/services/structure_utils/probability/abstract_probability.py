import logging
from abc import ABC, abstractmethod

logger = logging.getLogger(__name__)


class ProbabilityABC(ABC):
    """ProbabilityABC"""

    # def __init__(self):
    #     pass

    @classmethod
    @abstractmethod
    def from_db_model(cls, **data):
        raise NotImplementedError

    @abstractmethod
    def initialize_nan(self):
        raise NotImplementedError

    @abstractmethod
    def set_to_uniform(self):
        raise NotImplementedError

    @abstractmethod
    def normalize(self):
        raise NotImplementedError

    @abstractmethod
    def isnormalized(self):
        raise NotImplementedError

    @classmethod
    @abstractmethod
    def from_json(cls):
        raise NotImplementedError

    @abstractmethod
    def to_json(self):
        raise NotImplementedError

    def to_dict(self):
        raise NotImplementedError

    @abstractmethod
    def get_distribution(self, **kwargs):
        raise NotImplementedError

    @abstractmethod
    def to_pyagrum(self):
        raise NotImplementedError

    @abstractmethod
    def to_pycid(self):
        raise NotImplementedError
