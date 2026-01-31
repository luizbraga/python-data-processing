import logging

from openai import OpenAI

from app.config import settings
from app.llm.backends.base import LLMProvider

logger = logging.getLogger(__name__)


class OpenAIProvider(LLMProvider):
    """OpenAI GPT provider."""

    def __init__(self) -> None:
        if not settings.openai_api_key:
            raise ValueError("OPENAI_API_KEY not configured")
        self.client = OpenAI(api_key=settings.openai_api_key)

    async def generate_summary(self, prompt: str) -> str:
        """Generate summary using OpenAI API."""
        try:
            response = self.client.chat.completions.create(
                model=settings.llm_model,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a medical assistant helping to create concise, accurate patient summaries for healthcare providers.",
                    },
                    {"role": "user", "content": prompt},
                ],
                temperature=settings.llm_temperature,
                max_tokens=settings.llm_max_tokens,
            )
            return response.choices[0].message.content or ""
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
