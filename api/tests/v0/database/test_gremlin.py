from unittest.mock import patch

import pytest

from src.v0.database.gremlin import Builder, GremlinClient, Query, Response, get_client


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


def test_class_GremlinClient():
    client = GremlinClient("connection")
    assert client.graph_name == "g"
    assert isinstance(client.builder, Builder)


def test_GremlinClient_connect():
    client = GremlinClient("connection")
    assert client.connect() is None


def test_GremlinClient_close():
    class MockedClient:
        def close(self):
            return True

    client = GremlinClient("connection")
    client._client = MockedClient()
    # we run the close() method without returning it in the GremlinClient.close) method
    assert client.close() is None


@patch("src.v0.database.gremlin.client")
def test_mock_GremlinClient_execute_query_without_params(mocked_client):
    with GremlinClient("connection") as c:
        mock = mocked_client.return_value
        mock.submit.return_value = True
        assert c.execute_query("query")


@patch("src.v0.database.gremlin.client")
def test_mock_GremlinClient_execute_query_with_params(mocked_client):
    with GremlinClient("connection") as c:
        mock = mocked_client.return_value
        mock.submit.return_value = True
        assert c.execute_query("query", params={"key": True})


@patch("src.v0.database.gremlin.GremlinClient.connect")
def test_mock_GremlinClient_execute_query_fail(mocked_connection):
    mock = mocked_connection.return_value
    mock._client.return_value = True
    with pytest.raises(Exception) as exc:
        with GremlinClient("connection") as client:
            client.execute_query("query")
    assert "Not connected to the Gremlin Server." in str(exc.value)


def test_get_client():
    assert isinstance(get_client(), GremlinClient)
