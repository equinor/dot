from pydantic import AliasChoices, Field, constr, field_validator

from ... import DOTModel
from .meta import VertexMetaData, VertexMetaDataResponse


class SessionData(DOTModel):
    name: str
    description: str | None = None
    tag: list[str] | None = None
    owner: str | None = None
    shared: str = "True"
    index: str | None = None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "name": "this is an objective",
                    "description": "objectively objecting the objectives",
                    "tag": ["subsurface"],
                    "owner": "John Doe",
                    "shared": "True",
                    "index": "0",
                }
            ]
        }
    }

    @field_validator("shared")
    @classmethod
    def check_shared(cls, v: str) -> str:
        allowed_values = [
            "True",
            "False",
        ]
        if v not in allowed_values:
            raise ValueError("must be None or in True/False")
        return v


class Session(VertexMetaData, SessionData):
    pass


class SessionResponse(VertexMetaDataResponse, Session):
    id: str = Field(validation_alias=AliasChoices("T.id", "id"))
    label: constr(to_lower=True) = Field(
        validation_alias=AliasChoices("T.label", "label")
    )
