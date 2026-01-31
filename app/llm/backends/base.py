from abc import ABC, abstractmethod


class LLMProvider(ABC):
    """Abstract base class for LLM providers."""

    @abstractmethod
    async def generate_summary(self, prompt: str) -> str:
        """Generate a summary from the prompt."""
        pass
