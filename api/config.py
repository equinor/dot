import os
from pydantic import AnyHttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings): 
    default_database_address: str = 'database:8182'
    APP_ENVIRONMENT: str = os.getenv('APP_ENVIRONMENT', 'local')
    DB_PRIMARY_KEY: str = os.getenv('DB_PRIMARY_KEY', 'key')
    DATABASE_ADDRESS: str = os.getenv('DATABASE_ADDRESS', default_database_address)

    # frontend
    REACT_APP_WEB_HOST: str = "localhost"
    REACT_APP_WEB_PORT: str = "3000"

    # static cosmos parameters
    COSMOS_DB_NAME: str = "decisionDB"
    COSMOS_CONTAINER: str = "prototype"

    @computed_field
    def FRONTEND_URL(self) -> AnyHttpUrl:
        return f"http://{self.REACT_APP_WEB_HOST}:{self.REACT_APP_WEB_PORT}"


    @computed_field
    def DATABASE_URL(self) -> AnyHttpUrl:
        return f"http://{self.DATABASE_ADDRESS}"

    @computed_field
    def DATABASE_CONNECTION(self) -> str:
        
        if self.DATABASE_ADDRESS == self.default_database_address:
            return f"ws://{self.DATABASE_ADDRESS}/gremlin"
        else:
            return f"wss://{self.DATABASE_ADDRESS}/gremlin"

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
