# Reddit LLM Alerts

**DO NOT USE THIS FOR SPAMMING OR ANYTHING ILLEGAL.**

This project ist meant to make monitoring reddit easier, so that you as the creator of e.g. an open-source product can easily chime in and pitch it. But be honest, don't create fake reviews, etc.

This is a small Python application that monitors specific subreddits for posts containing certain keywords, and then uses the Anthropic API to analyze the relevance of these posts to a given project description.

**Note:** This project is 90+% AI generated, but I have used it successfully and fixed most major issues.

## Features

- Fetch recent posts from specified subreddits based on keywords
- Analyze post relevance using Anthropic's language model
- Configurable via environment variables or `.env` file
- Command-line interface for easy usage

## Prerequisites

Before you begin, ensure you have met the following requirements:

- Python 3.12 or higher
- Poetry for dependency management
- Reddit API credentials (client ID and client secret)
- Anthropic API key

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/reddit-llm-alerts.git
   cd reddit-llm-alerts
   ```

2. Install dependencies using Poetry:
   ```
   poetry install
   ```

## Configuration

Create a `.env` file in the root directory of the project with the following content:

```
REDDIT_CLIENT_ID=your_reddit_client_id
REDDIT_CLIENT_SECRET=your_reddit_client_secret
ANTHROPIC_API_KEY=your_anthropic_api_key
SUBREDDITS=["subreddit1", "subreddit2"]
KEYWORDS=["keyword1", "keyword2"]
PROJECT_DESCRIPTION="Your project description here"
```

Replace the placeholder values with your actual API credentials and desired configuration.

## Usage

To run the Reddit LLM Alerts:

```
poetry run run-alerts
```

You can also override the configuration settings from the command line:

```
poetry run run-alerts --subreddits programming python --keywords "machine learning" AI
```

## Development

### Running Tests

To run the test suite:

```
poetry run pytest
```

### Code Formatting and Linting

We use `ruff` for code formatting and linting. To check your code:

```
poetry run ruff format --check .
poetry run ruff check .
```

To automatically format your code:

```
poetry run ruff format .
```

### Type Checking

We use `mypy` for static type checking. Although there is currently a lot wrong with these, feel free to fix it. To run type checking:

```
poetry run mypy src tests
```

## License

This project is licensed under the Open Source for Humanity License (OSH License) version 1.1. This license allows usage for open-source projects and projects that benefit humanity, and permits modification as long as the same license terms are maintained.

Key points of the license include:
- The software must be used for open-source projects or projects that benefit humanity.
- Modifications must be distributed under the same license terms.
- **The software must not be used for spamming, illegal activities, or creating false/misleading information.**
- The intended use is to facilitate legitimate monitoring of public forums for open-source or humanitarian projects.

Users are required to engage in honest and transparent communication when using this software.

For full terms and conditions, see the [LICENSE.md](LICENSE.md) file in this repository.

## Contact

If you want to contact me, you can reach me at jascha@kviklet.dev.

## Acknowledgements

- Reddit API
- Anthropic API
- Claude 3.5 for building this, thanks!