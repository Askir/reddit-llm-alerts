from typing import Dict, List

import requests

from .models import RedditPost


class RedditClient:
    def __init__(self, client_id: str, client_secret: str, user_agent: str):
        self.client_id = client_id
        self.client_secret = client_secret
        self.user_agent = user_agent
        self.token = None
        self.base_url = "https://oauth.reddit.com"

    def _get_token(self):
        auth = requests.auth.HTTPBasicAuth(self.client_id, self.client_secret)
        data = {
            "grant_type": "client_credentials",
        }
        headers = {"User-Agent": self.user_agent}
        response = requests.post(
            "https://www.reddit.com/api/v1/access_token",
            auth=auth,
            data=data,
            headers=headers,
        )
        response.raise_for_status()
        self.token = response.json()["access_token"]

    def _make_request(self, endpoint: str, params: Dict = None) -> Dict:
        if not self.token:
            self._get_token()

        headers = {
            "Authorization": f"bearer {self.token}",
            "User-Agent": self.user_agent,
        }
        response = requests.get(f"{self.base_url}{endpoint}", headers=headers, params=params)
        response.raise_for_status()
        return response.json()

    def search_subreddit(self, subreddit: str, keywords: List[str], limit: int = 10) -> List[RedditPost]:
        query = " OR ".join(keywords)
        params = {
            "q": query,
            "restrict_sr": "on",  # Restrict search to subreddit
            "sort": "new",
            "limit": limit,
        }
        data = self._make_request(f"/r/{subreddit}/search.json", params)

        posts = []
        for post in data["data"]["children"]:
            post_data = post["data"]
            posts.append(
                RedditPost(
                    id=post_data["id"],
                    title=post_data["title"],
                    content=post_data["selftext"],
                    url=post_data["url"],
                    author=post_data["author"],
                    score=post_data["score"],
                    created_utc=post_data["created_utc"],
                    subreddit=post_data["subreddit"],
                )
            )

        return posts
