from gremlin_python.driver import client

from config import settings

from ..database.builders.queries.gremlin_queries_edge import (
    GremlinStringQueryBuilderEdge,
)
from ..database.builders.queries.gremlin_queries_vertex import (
    GremlinStringQueryBuilderVertex,
)
from ..database.builders.responses.gremlin_responses_edge import (
    GremlinResponseBuilderEdge,
)
from ..database.builders.responses.gremlin_responses_vertex import (
    GremlinResponseBuilderVertex,
)
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
        self.vertex = GremlinStringQueryBuilderVertex()
        self.edge = GremlinStringQueryBuilderEdge()


class Response(ResponseABC):
    def __init__(self):
        super().__init__()
        self.vertex = GremlinResponseBuilderVertex()
        self.edge = GremlinResponseBuilderEdge()


class Builder(BuilderABC):
    def __init__(self):
        super().__init__()
        self.query = Query()
        self.response = Response()


class GremlinClient(DatabaseClient):
    def __init__(self, connection, graph_name="g"):
        super().__init__(connection)
        self.graph_name = graph_name
        self.builder = Builder()

    def connect(self):
        self._client = client.Client(self.connection, self.graph_name)

    def close(self):
        if self._client:
            self._client.close()

    @catch_query_errors
    def execute_query(self, query, params=None):
        if not self._client:
            raise ConnectionError("Not connected to the Gremlin Server.")

        if params:
            results = self._client.submit(query, **params).all().result()
        else:
            results = self._client.submit(query).all().result()

        return results

    def __enter__(self):
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()


def get_client():
    return GremlinClient(settings.DATABASE_CONNECTION)
