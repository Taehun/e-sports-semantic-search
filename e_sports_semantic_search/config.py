from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PROJECT_NAME: str = "e-sports-semantic-search"
    DB_USER: str = "postgres"
    DB_PASS: str = "test"
    DB_NAME: str = "postgres"
    DB_HOST: str = "ci_db"
    DB_PORT: int = 5432
    X_API_KEY: str = "some_api_key"

    class Config:
        env_file = "./.env"


settings = Settings()
