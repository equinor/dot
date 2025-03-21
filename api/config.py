from pydantic import AnyHttpUrl, computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # frontend
    REACT_APP_WEB_HOST: str = "localhost"
    REACT_APP_WEB_PORT: str = "3000"

    @computed_field
    def FRONTEND_URL(self) -> AnyHttpUrl:
        return f"http://{self.REACT_APP_WEB_HOST}:{self.REACT_APP_WEB_PORT}"

    # database
    DATABASE_HOST: str = "database"  # instead of localhost
    DATABASE_PORT: str = "8182"

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
