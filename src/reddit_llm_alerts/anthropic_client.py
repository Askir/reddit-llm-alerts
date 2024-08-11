import logging
from typing import List

import anthropic

logger = logging.getLogger(__name__)


class AnthropicClient:
    def __init__(self, api_key: str):
        self.client = anthropic.Client(api_key=api_key)
        self.model = "claude-3-5-sonnet-20240620"  # You can change this to the specific model you want to use

    def analyze_relevance(self, post_content: str, project_description: str) -> bool:
        prompt = f"""
        Project Description: {project_description}

        Reddit Post Content: {post_content}

        Based on the project description and the content of the Reddit post,
        determine if this post is relevant to the project. 
        Be somewhat strict and take the project description at face value.
        Relevant is only a post that describes a problem that can be solved with the project.
        Or it discusses a solution that is similar to the project.
        Respond with only 'true' if the post is relevant, or 'false' if it is not relevant.
        """

        try:
            response = self.client.messages.create(
                model=self.model,
                max_tokens=1,
                temperature=0,
                messages=[{"role": "user", "content": prompt}],
            )

            # Extract the response content
            result = response.content[0].text.strip().lower()

            # Convert the string response to a boolean
            return result == "true"

        except anthropic.APIError as e:
            logger.error(f"Anthropic API error: {str(e)}")
            return False
        except Exception as e:
            logger.error(f"Unexpected error when analyzing post relevance: {str(e)}")
            return False

    def batch_analyze_relevance(self, posts: List[dict], project_description: str) -> List[bool]:
        return [self.analyze_relevance(post["content"], project_description) for post in posts]
