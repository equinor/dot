import time
from datetime import datetime
from uuid import UUID, uuid4

from pydantic import Field

from ... import DOTModel


class MetaData(DOTModel):
    """Metadata for database components. They are automatically generated."""

    version: str = "v0"
    """version of the database"""
    uuid: UUID = Field(default_factory=lambda: uuid4())
    """Unique identifier of the vertex"""


class VertexMetaData(MetaData):
    """Metadata for Vertices. They are automatically generated."""

    timestamp: float = Field(default_factory=lambda: time.time())
    """Timestamp at vertex creation"""
    date: datetime = Field(default_factory=lambda: datetime.now())
    """Date at vertex creation"""
    ids: str | None = "test"  # partition key for Azure cosmos DB
    """Partition key for Azure cosmos DB"""


class EdgeMetaData(MetaData):
    """Metadata for Edges. They are automatically generated."""

    pass


class VertexMetaDataResponse(VertexMetaData):
    uuid: str  # UUID     # TODO: fix the db uuid to real UUIDs
    timestamp: str  # float    # TODO: fix the db timestamp back to a float
    date: str  # datetime # TODO: fix the db dates to ISO format


class EdgeMetaDataResponse(EdgeMetaData):
    uuid: str  # UUID     # TODO: fix the db uuid to real UUIDs
