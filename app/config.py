# import os

# from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from .env file

# class Settings:
#     APP_ENV: str = os.getenv("APP_ENV", "development")

# settings = Settings()  

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"

 # Keeping Ollama as the default for local development.
    llm_provider: str = "ollama"
    model_name: str = "gemma3"

# Used only when llm_provider is "gemini".
    gemini_api_key: str | None = None
    gemini_model: str = "gemini-3.5-flash-lite"

    model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8",
      extra="ignore",
      )

settings = Settings()  # Create an instance of the Settings class
