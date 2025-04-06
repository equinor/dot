from typing import Any
from uuid import UUID, uuid4

from src.v0.services.classes.errors import (
    ArcLabelValidationError,
    EndPointValidationError,
    UUIDValidationError,
)
from src.v0.services.classes.node import NodeABC


def label(arg: Any) -> str:
    if not (isinstance(arg, str) or arg is None):
        raise ArcLabelValidationError(arg)
    return arg


def edge(arg: Any) -> NodeABC:
    if not (isinstance(arg, NodeABC) or arg is None):
        raise EndPointValidationError(arg)
    return arg


def uuid(arg: Any) -> str:
    if not (isinstance(arg, str | UUID) or arg is None):
        raise UUIDValidationError(arg)
    if arg is None:
        return str(uuid4())
    if isinstance(arg, UUID) and arg.version == 4:
        return str(arg)
    try:  # if arg is str
        uuid_obj = UUID(arg)
        if uuid_obj.version == 4:
            return arg
    except Exception as e:
        raise UUIDValidationError(e)
    raise UUIDValidationError(f"version {uuid_obj.version}")
