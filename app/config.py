# import os

# from dotenv import load_dotenv

# load_dotenv()  # Load environment variables from .env file

# class Settings:
#     APP_ENV: str = os.getenv("APP_ENV", "development")

# settings = Settings()  

from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    app_env: str = "development"
    model_name: str = "gemma3"

    model_config = SettingsConfigDict(
      env_file=".env",
      env_file_encoding="utf-8"
      )

settings = Settings()  # Create an instance of the Settings class
