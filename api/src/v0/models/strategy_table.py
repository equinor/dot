from pydantic import AliasChoices, Field, constr

from ... import DOTModel
from .meta import VertexMetaData, VertexMetaDataResponse


class Strategy(DOTModel):
    name: str
    rationale: str | None = None
    objective: str | None = None
    path: dict[str, str | None] | None = None
    symbole: str | None = None
    colour: str | None = None


class StrategyTableData(DOTModel):
    table: list[Strategy]


class StrategyTable(VertexMetaData, StrategyTableData):
    pass


class StrategyTableResponse(VertexMetaDataResponse, StrategyTable):
    id: str = Field(validation_alias=AliasChoices("T.id", "id"))
    label: constr(to_lower=True) = Field(
        validation_alias=AliasChoices("T.label", "label")
    )
