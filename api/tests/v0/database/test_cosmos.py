from unittest.mock import patch

import pytest

from src.v0.database.cosmos import (
    AzureCosmosClient,
    Builder,
    Query,
    Response,
    get_client,
)


def test_class_Query():
    query = Query()
    assert hasattr(query, "vertex")
    assert hasattr(query, "edge")


def test_class_Response():
    response = Response()
    assert hasattr(response, "vertex")
    assert hasattr(response, "edge")


def test_class_Builder():
    builder = Builder()
    assert hasattr(builder, "query")
    assert hasattr(builder, "response")


def test_class_AzureCosmosClient():
    client = AzureCosmosClient("connection", "credential", "database_name")
    assert client.credential == "credential"
    assert client.database_name == "database_name"
    assert client.database_container == "decisionItems"
    assert client._gremlin_client is None
    assert client._graph is None
    assert isinstance(client.builder, Builder)


def test_AzureCosmosClient_connect():
    client = AzureCosmosClient("connection", "credential", "database_name")
    assert client.connect() is None


def test_AzureCosmosClient_close():
    class MockedClient:
        def close(self):
            return True

    client = AzureCosmosClient("connection", "credential", "database_name")
    client._client = MockedClient()
    # we run the close() method without returning it in the GremlinClient.close) method
    assert client.close() is None


@patch("src.v0.database.cosmos.client")
def test_mock_GremlinClient_execute_query_without_params(mocked_client):
    with AzureCosmosClient("connection", "credential", "database_name") as c:
        mock = mocked_client.return_value
        mock.submit.return_value = True
        assert c.execute_query("query")


@patch("src.v0.database.cosmos.client")
def test_mock_GremlinClient_execute_query_with_params(mocked_client):
    with AzureCosmosClient("connection", "credential", "database_name") as c:
        mock = mocked_client.return_value
        mock.submit.return_value = True
        assert c.execute_query("query", params={"key": True})


@patch("src.v0.database.cosmos.AzureCosmosClient.connect")
def test_mock_GremlinClient_execute_query_fail(mocked_connection):
    mock = mocked_connection.return_value
    mock._client.return_value = True
    with pytest.raises(Exception) as exc:
        with AzureCosmosClient("connection", "credential", "database_name") as client:
            client.execute_query("query")
    assert "Not connected to the Azure CosmosDB Server." in str(exc.value)


def test_get_client():
    assert isinstance(get_client(), AzureCosmosClient)
