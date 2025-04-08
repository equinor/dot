import pytest

from src.v0.models.meta import EdgeMetaDataResponse, VertexMetaDataResponse
from src.v0.services.format_conversions.base import ConversionABC, MetadataCreate


def test_class_ConversionABC(monkeypatch):
    monkeypatch.setattr(
        ConversionABC,
        "__abstractmethods__",
        set(),
    )
    conversion = ConversionABC()
    with pytest.raises(NotImplementedError):
        conversion.from_json(None)
    with pytest.raises(NotImplementedError):
        conversion.to_json(None)


def test_MetadataCreate_vertex():
    metadata = MetadataCreate.vertex("1")
    assert isinstance(metadata, VertexMetaDataResponse)
    assert metadata.uuid == "1"
    assert metadata.version == "v0"


def test_MetadataCreate_edge():
    metadata = MetadataCreate.edge("1")
    assert isinstance(metadata, EdgeMetaDataResponse)
    assert metadata.uuid == "1"
