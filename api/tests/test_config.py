from config import settings


def test_config_settings_computed_fields():
    assert settings.FRONTEND_URL == "http://localhost:3000"
    # TODO: Expecting .env updates and new addresses coming in from Azure
    # assert settings.DATABASE_URL == "http://localhost:8182"
    # assert settings.DATABASE_CONNECTION == "ws://localhost:8182/gremlin"
    # assert settings.BACKEND_CORS_ORIGINS == [ "http://localhost:3000", "http://localhost:8182"]
