import os
from pydantic import AnyHttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    APP_ENVIRONMENT: str = os.getenv('APP_ENVIRONMENT', 'local')
    DB_PRIMARY_KEY: str = os.getenv('DB_PRIMARY_KEY', 'key')

    # frontend
    REACT_APP_WEB_HOST: str = "localhost"
    REACT_APP_WEB_PORT: str = "3000"
    COSMOS_DB_NAME: str = "decisionDB"
    COSMOS_CONTAINER: str = "decisionItems"

    @computed_field
    def DATABASE_HOST(self) -> str:
        if self.APP_ENVIRONMENT.lower().__contains__('local'):
            return 'database'
        return os.getenv('COSMOS_ACCOUNT_URL', '')
    
    @computed_field
    def DATABASE_PORT(self) -> str:
        if self.APP_ENVIRONMENT.lower().__contains__('local'):
            return '8182'
        return os.getenv('COSMOS_PORT', '')

    @computed_field
    def FRONTEND_URL(self) -> AnyHttpUrl:
        return f"http://{self.REACT_APP_WEB_HOST}:{self.REACT_APP_WEB_PORT}"


    @computed_field
    def DATABASE_URL(self) -> AnyHttpUrl:
        return f"http://{self.DATABASE_HOST}:{self.DATABASE_PORT}"

    @computed_field
    def DATABASE_CONNECTION(self) -> str:
        
        if self.DATABASE_HOST == "database":
            return f"ws://{self.DATABASE_HOST}:{self.DATABASE_PORT}/gremlin"
        else:
            return f"wss://{self.DATABASE_HOST}:{self.DATABASE_PORT}/gremlin"

    # backend
    @computed_field
    def BACKEND_CORS_ORIGINS(self) -> list[AnyHttpUrl]:
        return [self.FRONTEND_URL, self.DATABASE_URL]

    # general configuration settings
    model_config = SettingsConfigDict(
        # `.env.prod` takes priority over `.env`
        # env_file=('.env', '.env.prod')
        env_file=(".env")
    )


settings = Settings()
