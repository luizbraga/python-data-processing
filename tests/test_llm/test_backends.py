from unittest.mock import MagicMock, patch

import pytest

from app.config import settings
from app.llm.backends.openai import OpenAIProvider


class TestOpenAIProvider:
    def test_openai_provider_initialization(self) -> None:
        with (
            patch("app.llm.backends.openai.OpenAI") as mock_openai,
            patch("app.config.settings.openai_api_key", "test_api_key"),
        ):
            mock_openai.return_value = MagicMock()
            provider = OpenAIProvider()
            assert provider.client is not None
            mock_openai.assert_called_once_with(api_key="test_api_key")

    def test_openai_provider_initialization_no_api_key(self) -> None:
        with patch("app.config.settings.openai_api_key", None):
            with pytest.raises(ValueError, match="OPENAI_API_KEY not configured"):
                OpenAIProvider()

    @pytest.mark.asyncio
    async def test_generate_summary_success(self) -> None:
        with (
            patch("app.llm.backends.openai.OpenAI") as mock_openai,
            patch("app.config.settings.openai_api_key", "test_api_key"),
        ):
            mock_client = MagicMock()
            mock_client.chat.completions.create.return_value = MagicMock(
                choices=[MagicMock(message=MagicMock(content="Test summary"))]
            )
            mock_openai.return_value = mock_client

            provider = OpenAIProvider()
            summary = await provider.generate_summary("Test prompt")
            assert summary == "Test summary"
            mock_client.chat.completions.create.assert_called_once_with(
                model=settings.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical assistant helping to create concise, accurate patient summaries for healthcare providers.",
                    },
                    {"role": "user", "content": "Test prompt"},
                ],
            )
