from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_SERVICE_KEY: str
    jwt_secret: str
    jwt_algorithm: str = "HS256"

    # This line tells Pydantic to read from your .env file
    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()