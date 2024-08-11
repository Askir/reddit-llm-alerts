import argparse
import logging
from datetime import datetime
from typing import List

from pydantic import BaseModel

from reddit_llm_alerts.anthropic_client import AnthropicClient
from reddit_llm_alerts.config import config
from reddit_llm_alerts.models import RedditPost, RelevanceResult
from reddit_llm_alerts.reddit_client import RedditClient

import json


def setup_logging():
    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def store_reddit_posts_in_file(posts: List[RedditPost], file_path: str):
    """
    Store Reddit posts in a json file for later prompt engineering tests
    :param posts:
    :param file_path:
    :return:
    """
    class RedditPostList(BaseModel):
        posts: List[RedditPost]

    posts = RedditPostList(posts=posts)

    with open(file_path, 'w') as f:
        f.write(posts.model_dump_json(indent=2))


def fetch_posts(reddit_client: RedditClient, subreddits: List[str], keywords: List[str]) -> List[RedditPost]:
    all_posts = []
    for subreddit in subreddits:
        posts = reddit_client.search_subreddit(subreddit, keywords, max_time_back_in_hours=config.hours)
        all_posts.extend(posts)
    return all_posts


def analyze_posts(anthropic_client: AnthropicClient, posts: List[RedditPost]) -> List[RelevanceResult]:
    logger = logging.getLogger(__name__)
    results = []
    for post in posts:
        logger.debug(f"Analyzing post: {post.title} - {post.url}")
        is_relevant = anthropic_client.analyze_relevance(post.content, config.project_description)
        logger.debug(f"Is relevant: {is_relevant}")
        results.append(RelevanceResult(post=post, is_relevant=is_relevant))
    return results


def display_results(results: List[RelevanceResult]):
    relevant_posts = [result for result in results if result.is_relevant]
    print(f"Found {len(relevant_posts)} relevant posts out of {len(results)} total posts:")
    for result in relevant_posts:
        post = result.post
        print(f"\nTitle: {post.title}")
        print(f"Subreddit: r/{post.subreddit}")
        print(f"URL: {post.url}")
        print(f"Score: {post.score}")
        print(f"Created at: {post.created_at}")
        print("-" * 40)


def main():
    parser = argparse.ArgumentParser(description="Reddit LLM Alerts")
    parser.add_argument(
        "--subreddits",
        nargs="+",
        default=config.subreddits,
        help="List of subreddits to search",
    )
    parser.add_argument(
        "--keywords",
        nargs="+",
        default=config.keywords,
        help="List of keywords to search for",
    )
    args = parser.parse_args()

    setup_logging()
    logger = logging.getLogger(__name__)

    reddit_client = RedditClient(
        client_id=config.reddit_client_id,
        client_secret=config.reddit_client_secret,
        user_agent=config.reddit_user_agent,
    )
    anthropic_client = AnthropicClient(api_key=config.anthropic_api_key, model=config.model)

    logger.info("Fetching posts from Reddit...")
    posts = fetch_posts(reddit_client, args.subreddits, args.keywords)
    logger.info(f"Fetched {len(posts)} posts")
    logger.info("Storing posts in a file...")
    date_file_path = f"reddit_posts_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    store_reddit_posts_in_file(posts, date_file_path)

    logger.info("Analyzing posts with Anthropic API...")
    results = analyze_posts(anthropic_client, posts)

    display_results(results)


if __name__ == "__main__":
    main()
