"""
General utilities fo data format conversions between database and service layer-
"""
import datetime
from abc import ABC, abstractmethod

from src.v0.models.meta import EdgeMetaDataResponse, VertexMetaDataResponse


class ConversionABC(ABC):
    """
    Abstract class for data format conversions between database and service layer.
    """
    @abstractmethod
    def to_json(self, data):
        raise NotImplementedError

    @abstractmethod
    def from_json(self, data):
        raise NotImplementedError


class MetadataCreate:
    """
    Creation of metadata response
    """
    def vertex(uuid: str) -> VertexMetaDataResponse:
        """Create metadata for vertex

        Args:
            uuid (str): UUID of vertex as string

        Returns:
            VertexMetaDataResponse: vertex metadata
        """
        version = "v0"
        ct = datetime.datetime.now()
        date = str(ct)
        timestamp = str(ct.timestamp())
        uuid = uuid
        return VertexMetaDataResponse.model_validate(
            {
            "version": version,
            "date": date,
            "timestamp": timestamp,
            "uuid": uuid
            }
        )

    def edge(uuid: str) -> EdgeMetaDataResponse:
        """Create metadata for edge

        Args:
            uuid (str): UUID of edge as string

        Returns:
            EdgeMetaDataResponse: edge metadata

        """
        version = "v0"
        uuid = uuid
        return EdgeMetaDataResponse.model_validate(
            {
            "version": version,
            "uuid": uuid
            }
        )
