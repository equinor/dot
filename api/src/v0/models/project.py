from pydantic import AliasChoices, ConfigDict, Field, constr

from ... import DOTModel
from .meta import VertexMetaDataResponse


class ProjectCreate(DOTModel):
    """Project data model"""

    name: str | None
    """Name of the project"""
    description: str | None = None
    """Description of the project"""
    tag: list[str] | None = None
    """List of user input keywords"""
    decision_maker: str | None = None
    """Name of the decision maker"""
    decision_date: str | None = None
    """Date by which the project needs to be ended"""
    sensitivity_label: str | None = "Restricted"
    """Security level of the project (Open, Internal, Restricted, Confidential)"""
    index: str | None = None
    """Index of the project"""

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "name": "the little project example",
                    "description": "This is a project example",
                    "tag": "subsurface",
                    "decision_maker": "John Doe",
                    "decision_date": "2021-01-01",
                    "sensitivity_label": "Restricted",
                    "index": "0",
                }
            ]
        },
    )


class ProjectUpdate(DOTModel):
    name: str | None = None
    tag: list[str] | None = None
    description: str | None = None
    index: str | None = None
    decision_maker: str | None = None
    decision_date: str | None = None
    sensitivity_label: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "tag": "subsurface",
                    "index": "0",
                    "name": "the little project example",
                    "description": "This is a project example",
                    "decision_maker": "John Doe",
                    "decision_date": "2021-01-01",
                    "sensitivity_label": "Restricted",
                }
            ]
        },
    )


class ProjectResponse(VertexMetaDataResponse):
    name: str
    description: str | None
    tag: list[str] | None
    decision_maker: str | None
    decision_date: str | None
    sensitivity_label: str | None
    index: str | None

    id: str = Field(validation_alias=AliasChoices("T.id", "id"))
    label: constr(to_lower=True) = Field(
        validation_alias=AliasChoices("T.label", "label")
    )

    model_config = ConfigDict(
        json_schema_extra={
            "examples": [
                {
                    "tag": "subsurface",
                    "index": "0",
                    "name": "the little project example",
                    "description": "This is a project example",
                    "decision_maker": "John Doe",
                    "decision_date": "2021-01-01",
                    "sensitivity_label": "Restricted",
                }
            ]
        },
    )
