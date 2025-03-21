from pydantic import AliasChoices, ConfigDict, Field, constr

from ... import DOTModel
from .meta import VertexMetaDataResponse


class OpportunityCreate(DOTModel):
    """Opportunity data model"""

    description: str
    """Description of the opportunity"""
    tag: list[str] | None = None
    """List of user input keywords"""
    index: str | None = None
    """Index of the opportunity"""

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "description": "opportunistic opportunity",
                    "tag": ["subsurface"],
                    "index": "0",
                }
            ]
        }
    }


class OpportunityUpdate(DOTModel):
    description: str | None = None
    tag: list[str] | None = None
    index: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "tag": ["subsurface"],
                    "index": "0",
                    "description": "opportunistic opportunity",
                }
            ]
        }
    }


class OpportunityResponse(VertexMetaDataResponse):
    description: str
    tag: list[str] | None
    index: str | None

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
                }
            ]
        },
    )
