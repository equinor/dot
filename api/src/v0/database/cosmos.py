from azure.cosmos.aio import CosmosClient
from gremlin_python.driver import client, serializer

from config import settings

from ..database.client import (
    BuilderABC,
    DatabaseClient,
    QueryABC,
    ResponseABC,
    catch_query_errors,
)


class Query(QueryABC):
    def __init__(self):
        super().__init__()
        self.vertex = None
        self.edge = None


class Response(ResponseABC):
    def __init__(self):
        super().__init__()
        self.vertex = None
        self.edge = None


class Builder(BuilderABC):
    def __init__(self):
        super().__init__()
        self.query = Query()
        self.response = Response()


class AzureCosmosClient(DatabaseClient):
    def __init__(self, connection, credential, database_name):
        super().__init__(connection)
        self.credential = credential  # primary key from Secret
        self.database_name = database_name  # settings.DATABASE_NAME
        self.database_container = "decisionItems"
        self._gremlin_client = None
        self._graph = None
        self.builder = Builder()

    def connect(self):
        self._client = CosmosClient(self.connection, self.credential)
        # self._graph = \
        #   self._client.get_database_client(self.database_name)\
        #   .get_graph(self.graph_name)
        # db = self._client.get_database_client(self.database_name)
        # container = db.get_container_client(self.database_container)
        self._gremlin_client = client.Client(
            self.connection,
            traversal_source="g",
            username=f"/dbs/{self.database_name}/colls/{self.database_container}",
            password=self.credential,
            message_serializer=serializer.GraphSONSerializersV2d0(),
        )

    def close(self):
        if self._gremlin_client:
            self._gremlin_client.close()

    @catch_query_errors
    def execute_query(self, query, params=None):
        # this should be the gremlin python client
        """self._gremlin_client = client.Client(
            self.connection,
            traversal_source="g",
            username=f"/dbs/{self.database_name}/colls/{self.database_container}",
            password=self.credential,
            message_serializer=serializer.GraphSONSerializersV2d0(),
        )"""

        if not self._gremlin_client:
            raise ConnectionError("Not connected to the Azure CosmosDB Server.")

        if params:
            results = self._gremlin_client.submit(query, **params).all().result()
        else:
            results = self._gremlin_client.submit(query).all().result()

        return results

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_client():
    return AzureCosmosClient(
        settings.DATABASE_CONNECTION,
        credential="myKey",
        database_name="decisionDB",
    )
