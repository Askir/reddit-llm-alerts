import pytest
from unittest.mock import patch, MagicMock
from reddit_llm_alerts.models import RedditPost, RelevanceResult
from scripts.run_alerts import fetch_posts, analyze_posts, display_results

@pytest.fixture
def mock_reddit_client():
    client = MagicMock()
    client.search_subreddit.return_value = [
        RedditPost(id="1", title="Test 1", content="Content 1", url="url1", author="author1", score=10, created_utc=1620000000, subreddit="sub1"),
        RedditPost(id="2", title="Test 2", content="Content 2", url="url2", author="author2", score=20, created_utc=1620000001, subreddit="sub2")
    ]
    return client

@pytest.fixture
def mock_anthropic_client():
    client = MagicMock()
    client.analyze_relevance.side_effect = [True, False]
    return client

def test_fetch_posts(mock_reddit_client):
    posts = fetch_posts(mock_reddit_client, ["sub1", "sub2"], ["keyword1", "keyword2"])
    assert len(posts) == 4  # 2 posts per subreddit
    mock_reddit_client.search_subreddit.assert_any_call("sub1", ["keyword1", "keyword2"])
    mock_reddit_client.search_subreddit.assert_any_call("sub2", ["keyword1", "keyword2"])

def test_analyze_posts(mock_anthropic_client):
    posts = [
        RedditPost(id="1", title="Test 1", content="Content 1", url="url1", author="author1", score=10, created_utc=1620000000, subreddit="sub1"),
        RedditPost(id="2", title="Test 2", content="Content 2", url="url2", author="author2", score=20, created_utc=1620000001, subreddit="sub2")
    ]
    results = analyze_posts(mock_anthropic_client, posts)
    assert len(results) == 2
    assert results[0].is_relevant == True
    assert results[1].is_relevant == False

def test_display_results(capsys):
    results = [
        RelevanceResult(post=RedditPost(id="1", title="Test 1", content="Content 1", url="url1", author="author1", score=10, created_utc=1620000000, subreddit="sub1"), is_relevant=True),
        RelevanceResult(post=RedditPost(id="2", title="Test 2", content="Content 2", url="url2", author="author2", score=20, created_utc=1620000001, subreddit="sub2"), is_relevant=False)
    ]
    display_results(results)
    captured = capsys.readouterr()
    assert "Found 1 relevant posts out of 2 total posts:" in captured.out
    assert "Title: Test 1" in captured.out
    assert "Title: Test 2" not in captured.out