import pytest
from unittest.mock import patch, MagicMock
from reddit_llm_alerts.reddit_client import RedditClient
from reddit_llm_alerts.models import RedditPost


@pytest.fixture
def reddit_client():
    return RedditClient("test_client_id", "test_client_secret", "test_user_agent")


def test_get_token(reddit_client):
    with patch('requests.post') as mock_post:
        mock_post.return_value.json.return_value = {"access_token": "test_token"}
        reddit_client._get_token()
        assert reddit_client.token == "test_token"


def test_search_subreddit(reddit_client):
    with patch.object(reddit_client, '_make_request') as mock_request:
        mock_request.return_value = {
            "data": {
                "children": [
                    {
                        "data": {
                            "id": "test_id",
                            "title": "Test Title",
                            "selftext": "Test Content",
                            "url": "https://reddit.com/test",
                            "author": "test_author",
                            "score": 100,
                            "created_utc": 1620000000,
                            "subreddit": "test_subreddit"
                        }
                    }
                ]
            }
        }

        results = reddit_client.search_subreddit("test_subreddit", ["test", "keyword"])

        assert len(results) == 1
        assert isinstance(results[0], RedditPost)
        assert results[0].id == "test_id"
        assert results[0].title == "Test Title"
        assert results[0].content == "Test Content"
        assert results[0].url == "https://reddit.com/test"
        assert results[0].author == "test_author"
        assert results[0].score == 100
        assert results[0].created_utc == 1620000000
        assert results[0].subreddit == "test_subreddit"


def test_make_request(reddit_client):
    with patch.object(reddit_client, '_get_token'), patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"test": "data"}
        result = reddit_client._make_request("/test_endpoint")
        assert result == {"test": "data"}