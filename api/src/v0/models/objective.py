from pydantic import AliasChoices, ConfigDict, Field, constr

from ... import DOTModel
from .meta import VertexMetaDataResponse


class ObjectiveCreate(DOTModel):
    """Objective data model"""

    description: str
    """Description of the opportunity"""
    hierarchy: str | None = None
    """Hierarchy of the opportunity (Strategic, Fundamental, Mean)"""
    tag: list[str] | None = None
    """List of user input keywords"""
    index: str | None = None
    """Index of the objective"""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "description": "objectively objecting the objectives",
                    "hierarchy": "Fundamental",
                    "tag": ["subsurface"],
                    "index": "0",
                }
            ]
        },
    )


class ObjectiveUpdate(DOTModel):
    description: str | None = None
    tag: list[str] | None = None
    index: str | None = None
    hierarchy: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "description": "objectively objecting the objectives",
                    "tag": ["subsurface"],
                    "index": "0",
                    "hierarchy": "Fundamental",
                }
            ]
        },
    )


class ObjectiveResponse(VertexMetaDataResponse):
    description: str
    tag: list[str] | None
    index: str | None
    hierarchy: str | None

    id: str = Field(validation_alias=AliasChoices("T.id", "id"))
    label: constr(to_lower=True) = Field(
        validation_alias=AliasChoices("T.label", "label")
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "description": "objectively objecting the objectives",
                    "tag": ["subsurface"],
                    "index": "0",
                    "hierarchy": "Fundamental",
                }
            ]
        },
    )
