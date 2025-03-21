from pydantic import AliasChoices, ConfigDict, Field, constr

from ... import DOTModel
from .meta import VertexMetaDataResponse


class VertexCreate(DOTModel):
    model_config = ConfigDict(
        extra="allow",
    )


class VertexUpdate(DOTModel):
    model_config = ConfigDict(
        extra="allow",
    )


class VertexResponse(VertexMetaDataResponse):
    id: str = Field(validation_alias=AliasChoices("T.id", "id"))
    label: constr(to_lower=True) = Field(
        validation_alias=AliasChoices("T.label", "label")
    )

    model_config = ConfigDict(
        extra="allow",
    )
