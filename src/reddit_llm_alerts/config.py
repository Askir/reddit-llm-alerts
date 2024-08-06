from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Config(BaseSettings):
    # Reddit API settings
    reddit_client_id: str
    reddit_client_secret: str
    reddit_user_agent: str = "RedditLLMAlerts/1.0"

    # Anthropic API settings
    anthropic_api_key: str

    # Application settings
    subreddits: List[str]
    keywords: List[str]
    project_description: str
    log_level: str = "INFO"

    # Optional: Database settings (if you decide to add database functionality later)
    # db_url: str = "sqlite:///./reddit_alerts.db"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Create a global instance of the Config class
config = Config()
