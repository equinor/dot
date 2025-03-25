from config import settings
from .client import DatabaseClient
from .cosmos import get_client as get_cosmos_client
from .gremlin import get_client as get_gremlin_client

# switch database configuration based on environment
def get_client() -> DatabaseClient:
    if settings.APP_ENVIRONMENT.lower().__contains__('local'):
        return get_gremlin_client()
    else:
        return get_cosmos_client()