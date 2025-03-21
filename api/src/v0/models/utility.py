from pydantic import AliasChoices, Field, constr

from ... import DOTModel
from .meta import VertexMetaData, VertexMetaDataResponse


class DiscreteUtilityData(DOTModel):
    parents_uuid: list[str]
    values: list[list[float]]


class ContinuousUtilityData(DOTModel):
    parents_uuid: list[str]


class UtilityData(DOTModel):
    dtype: DiscreteUtilityData | ContinuousUtilityData | None = None
    unit: str | None = None


class Utility(VertexMetaData, UtilityData):
    pass


class UtilityResponse(VertexMetaDataResponse, Utility):
    id: str = Field(validation_alias=AliasChoices("T.id", "id"))
    label: constr(to_lower=True) = Field(
        validation_alias=AliasChoices("T.label", "label")
    )
