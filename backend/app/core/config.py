from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Schedule API"
    DATABASE_URL: str = "postgresql+psycopg2://postegres:postgres@db:5432/schedule_db"

    class Config:
        env_file = ".env"

settings = Settings()