from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    Central application configuration.

    Values are loaded from environment variables and, when present,
    from the local .env file.
    """

    # ---------------------------------------------------------
    # Application
    # ---------------------------------------------------------

    app_name: str = "AI Resume Analyzer & Intelligent Job Matcher"
    app_version: str = "1.0.0"
    environment: str = "development"

    # ---------------------------------------------------------
    # Database
    # ---------------------------------------------------------

    database_url: str = ""

    # ---------------------------------------------------------
    # Generative AI
    # ---------------------------------------------------------

    llm_provider: str = ""
    llm_api_key: str = ""
    llm_model: str = ""

    # ---------------------------------------------------------
    # Embeddings
    # ---------------------------------------------------------

    embedding_model: str = ""

    # ---------------------------------------------------------
    # Logging
    # ---------------------------------------------------------

    log_level: str = "INFO"

    # ---------------------------------------------------------
    # Pydantic Settings Configuration
    # ---------------------------------------------------------

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )


@lru_cache
def get_settings() -> Settings:
    """
    Return a cached application settings instance.

    Caching prevents repeatedly loading configuration
    throughout the application lifecycle.
    """
    return Settings()