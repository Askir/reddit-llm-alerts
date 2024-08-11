import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
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


def create_mock_post(id, title, created_utc):
    return {
        "data": {
            "id": id,
            "title": title,
            "selftext": f"Content {id}",
            "url": f"https://reddit.com/r/test/{id}",
            "author": f"author{id}",
            "score": 100,
            "created_utc": created_utc,
            "subreddit": "test_subreddit"
        }
    }


def test_search_subreddit(reddit_client):
    with patch.object(reddit_client, '_make_request') as mock_request, \
            patch('reddit_llm_alerts.reddit_client.datetime') as mock_datetime:
        now = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.utcnow.return_value = now
        mock_datetime.fromtimestamp.side_effect = lambda x: datetime.fromtimestamp(x)

        three_days_ago = (now - timedelta(days=3)).timestamp()
        two_days_ago = (now - timedelta(days=2)).timestamp()
        one_day_ago = (now - timedelta(days=1)).timestamp()

        mock_request.return_value = {
            "data": {
                "children": [
                    create_mock_post("1", "Recent Post 1", now.timestamp()),
                    create_mock_post("2", "Recent Post 2", one_day_ago),
                    create_mock_post("3", "Two Days Old Post", two_days_ago),
                    create_mock_post("4", "Old Post", three_days_ago)
                ]
            }
        }

        results = reddit_client.search_subreddit("test_subreddit", ["test", "keyword"])

        assert len(results) == 3  # Now includes posts from exactly 2 days ago
        assert results[0].id == "1"
        assert results[1].id == "2"
        assert results[2].id == "3"
        assert all(isinstance(post, RedditPost) for post in results)


def test_search_subreddit_no_recent_posts(reddit_client):
    with patch.object(reddit_client, '_make_request') as mock_request, \
            patch('reddit_llm_alerts.reddit_client.datetime') as mock_datetime:
        now = datetime(2023, 1, 1, 12, 0, 0)
        mock_datetime.utcnow.return_value = now
        mock_datetime.fromtimestamp.side_effect = lambda x: datetime.fromtimestamp(x)

        three_days_ago = (now - timedelta(days=3)).timestamp()

        mock_request.return_value = {
            "data": {
                "children": [
                    create_mock_post("1", "Old Post 1", three_days_ago),
                    create_mock_post("2", "Old Post 2", three_days_ago - 3600),
                ]
            }
        }

        results = reddit_client.search_subreddit("test_subreddit", ["test", "keyword"])

        assert len(results) == 0  # No posts should be returned as they're all too old


def test_make_request(reddit_client):
    with patch.object(reddit_client, '_get_token'), patch('requests.get') as mock_get:
        mock_get.return_value.json.return_value = {"test": "data"}
        result = reddit_client._make_request("/test_endpoint")
        assert result == {"test": "data"}