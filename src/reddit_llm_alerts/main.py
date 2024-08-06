import logging
from typing import List, Dict

from .reddit_client import RedditClient
from .anthropic_client import AnthropicClient
from .config import Config
from .models import RedditPost, RelevanceResult

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def fetch_reddit_posts(
    reddit_client: RedditClient, subreddits: List[str], keywords: List[str]
) -> List[RedditPost]:
    """
    Fetch posts from specified subreddits containing given keywords.
    """
    posts = []
    for subreddit in subreddits:
        subreddit_posts = reddit_client.search_subreddit(subreddit, keywords)
        posts.extend(subreddit_posts)
    return posts


def analyze_posts(
    anthropic_client: AnthropicClient, posts: List[RedditPost], project_description: str
) -> List[RelevanceResult]:
    """
    Analyze the relevance of each post for the given project using the Anthropic API.
    """
    results = []
    for post in posts:
        relevance = anthropic_client.analyze_relevance(
            post.content, project_description
        )
        results.append(RelevanceResult(post=post, is_relevant=relevance))
    return results


def filter_relevant_posts(results: List[RelevanceResult]) -> List[RedditPost]:
    """
    Filter and return only the relevant posts.
    """
    return [result.post for result in results if result.is_relevant]


def main():
    config = Config()
    reddit_client = RedditClient(config.reddit_api_key)
    anthropic_client = AnthropicClient(config.anthropic_api_key)

    logger.info("Fetching posts from Reddit...")
    posts = fetch_reddit_posts(reddit_client, config.subreddits, config.keywords)
    logger.info(f"Fetched {len(posts)} posts")

    logger.info("Analyzing posts with Anthropic API...")
    results = analyze_posts(anthropic_client, posts, config.project_description)

    relevant_posts = filter_relevant_posts(results)
    logger.info(f"Found {len(relevant_posts)} relevant posts")

    # Here you can add logic to handle the relevant posts (e.g., save to database, send notifications)
    for post in relevant_posts:
        logger.info(f"Relevant post: {post.title}")


if __name__ == "__main__":
    main()
