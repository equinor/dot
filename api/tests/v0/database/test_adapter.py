from src.v0.database.gremlin import GremlinClient
from src.v0.database.cosmos import AzureCosmosClient

def test_get_client_local_environment(monkeypatch):
    monkeypatch.setenv('APP_ENVIRONMENT', 'local')
    from src.v0.database.adapter import get_client
    client = get_client()
    assert isinstance(client, GremlinClient)

def test_get_client_dev_environment(monkeypatch):
    monkeypatch.setenv('APP_ENVIRONMENT', 'dev')
    from src.v0.database.adapter import get_client
    client = get_client()
    assert isinstance(client, AzureCosmosClient)