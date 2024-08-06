from unittest.mock import patch, MagicMock
from reddit_llm_alerts.anthropic_client import AnthropicClient


def test_analyze_relevance():
    with patch('anthropic.Client') as MockClient:
        mock_client = MockClient.return_value
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="true")]
        mock_client.messages.create.return_value = mock_response

        # Create the AnthropicClient instance after patching
        anthropic_client = AnthropicClient("test_api_key")

        result = anthropic_client.analyze_relevance("Test content", "Test project")

        assert result is True
        mock_client.messages.create.assert_called_once()


def test_analyze_relevance_false():
    with patch('anthropic.Client') as MockClient:
        mock_client = MockClient.return_value
        mock_response = MagicMock()
        mock_response.content = [MagicMock(text="false")]
        mock_client.messages.create.return_value = mock_response

        # Create the AnthropicClient instance after patching
        anthropic_client = AnthropicClient("test_api_key")

        result = anthropic_client.analyze_relevance("Test content", "Test project")

        assert result is False


def test_batch_analyze_relevance():
    with patch('anthropic.Client'):
        anthropic_client = AnthropicClient("test_api_key")

        with patch.object(anthropic_client, 'analyze_relevance') as mock_analyze:
            mock_analyze.side_effect = [True, False, True]

            posts = [
                {"content": "Test 1"},
                {"content": "Test 2"},
                {"content": "Test 3"}
            ]

            results = anthropic_client.batch_analyze_relevance(posts, "Test project")

            assert results == [True, False, True]
            assert mock_analyze.call_count == 3