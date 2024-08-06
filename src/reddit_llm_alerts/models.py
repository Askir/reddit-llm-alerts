from pydantic import BaseModel
from datetime import datetime


class RedditPost(BaseModel):
    id: str
    title: str
    content: str
    url: str
    author: str
    score: int
    created_utc: float
    subreddit: str

    @property
    def created_at(self) -> datetime:
        return datetime.fromtimestamp(self.created_utc)


class RelevanceResult(BaseModel):
    post: RedditPost
    is_relevant: bool
