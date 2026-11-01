import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SUPABASE_URL: str
    SUPABASE_KEY: str
    GEMINI_API_KEY: str

    EVOLUTION_API_URL: str
    EVOLUTION_API_KEY: str
    EVOLUTION_INSTANCE_NAME: str

    MARKETPLACE_API_KEY: str = ""
    SUPPLIER_NUMBER: str = "5511999999999"

    class Config:
        env_file = ".env"

settings = Settings()
