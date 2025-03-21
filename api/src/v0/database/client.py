from abc import ABC, abstractmethod
from functools import wraps


def catch_query_errors(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            raise Exception(f"Error {e}: {args}, {kwargs}")

    return wrapper


class QueryABC(ABC):
    """
    This is defined as an Abstract class (although without abstract method) as we are
    not supposed to instantiate it.
    """

    def __init__(self):
        self.vertex = None
        self.edge = None


class ResponseABC(ABC):
    """
    This is defined as an Abstract class (although without abstract method) as we are
    not supposed to instantiate it.
    """

    def __init__(self):
        self.vertex = None
        self.edge = None


class BuilderABC(ABC):
    """
    This is defined as an Abstract class (although without abstract method) as we are
    not supposed to instantiate it.
    """

    def __init__(self):
        self.query = QueryABC()
        self.response = ResponseABC()


class DatabaseClient(ABC):
    def __init__(self, connection):
        self.connection = connection
        self._session = None
        self._client = None
        self.builder = None

    @abstractmethod
    def connect(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError

    @abstractmethod
    def execute_query(self, query, params=None):
        raise NotImplementedError
