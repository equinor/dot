import pytest

from src.v0.database.client import DatabaseClient


def test_database_client_methods(monkeypatch):
    monkeypatch.setattr(
        DatabaseClient,
        "__abstractmethods__",
        set(),
    )
    client = DatabaseClient("junk")

    with pytest.raises(NotImplementedError):
        client.connect()

    with pytest.raises(NotImplementedError):
        client.close()

    with pytest.raises(NotImplementedError):
        client.execute_query("query")
