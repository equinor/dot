from ... import DOTModel


class Filter(DOTModel):
    category: str | None = None
    hierarchy: str | None = None
    tag: str | None = None
    shortname: str | None = None
    name: str | None = None
    decisionType: str | None = None
    keyUncertainty: str | None = None
    boundary: str | None = None
