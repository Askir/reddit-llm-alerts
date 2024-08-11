from typing import List

from pydantic_settings import BaseSettings, SettingsConfigDict


class Config(BaseSettings):
    # Reddit API settings
    reddit_client_id: str = "dummy_client_id"
    reddit_client_secret: str = "dummy_client_secret"
    reddit_user_agent: str = "RedditLLMAlerts/1.0"
    anthropic_api_key: str = "dummy_api_key"
    subreddits: List[str] = ["AskReddit", "news"]
    keywords: List[str] = ["AI", "machine learning"]
    project_description: str = "A project to monitor Reddit for AI-related discussions"
    hours: int = 24
    model: str = "claude-3-5-sonnet-20240620"
    log_level: str = "INFO"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


# Create a global instance of the Config class
config = Config()
