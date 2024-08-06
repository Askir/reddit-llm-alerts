import argparse
import logging
from typing import List

from reddit_llm_alerts.config import config
from reddit_llm_alerts.reddit_client import RedditClient
from reddit_llm_alerts.anthropic_client import AnthropicClient
from reddit_llm_alerts.models import RedditPost, RelevanceResult


def setup_logging():
    logging.basicConfig(
        level=config.log_level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )


def fetch_posts(
    reddit_client: RedditClient, subreddits: List[str], keywords: List[str]
) -> List[RedditPost]:
    all_posts = []
    for subreddit in subreddits:
        posts = reddit_client.search_subreddit(subreddit, keywords)
        all_posts.extend(posts)
    return all_posts


def analyze_posts(
    anthropic_client: AnthropicClient, posts: List[RedditPost]
) -> List[RelevanceResult]:
    results = []
    for post in posts:
        is_relevant = anthropic_client.analyze_relevance(
            post.content, config.project_description
        )
        results.append(RelevanceResult(post=post, is_relevant=is_relevant))
    return results


def display_results(results: List[RelevanceResult]):
    relevant_posts = [result for result in results if result.is_relevant]
    print(
        f"Found {len(relevant_posts)} relevant posts out of {len(results)} total posts:"
    )
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
    anthropic_client = AnthropicClient(api_key=config.anthropic_api_key)

    logger.info("Fetching posts from Reddit...")
    posts = fetch_posts(reddit_client, args.subreddits, args.keywords)
    logger.info(f"Fetched {len(posts)} posts")

    logger.info("Analyzing posts with Anthropic API...")
    results = analyze_posts(anthropic_client, posts)

    display_results(results)


if __name__ == "__main__":
    main()
