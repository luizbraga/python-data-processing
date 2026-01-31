import logging
from datetime import datetime

from app.config import settings
from app.llm.backends.base import LLMProvider
from app.llm.backends.openai import OpenAIProvider
from app.llm.exceptions import SummaryGenerationError
from app.llm.prompts import PATIENT_NOTES_SUMMARY_PROMPT

logger = logging.getLogger(__name__)


class LLMService:
    """Service for interacting with LLM providers."""

    def __init__(self) -> None:
        self.provider = self._get_provider()

    def _get_provider(self) -> LLMProvider:
        backend_mapping: dict[str, type[LLMProvider]] = {
            "openai": OpenAIProvider,
        }
        backend = backend_mapping.get(settings.llm_provider)
        if not backend:
            raise ValueError(f"Unknown LLM provider: {settings.llm_provider}")
        return backend()

    def _calculate_age(self, date_of_birth: str) -> int:
        """Calculate age from date of birth string (YYYY-MM-DD)."""
        try:
            birth_date = datetime.strptime(date_of_birth, "%Y-%m-%d")
            today = datetime.now()
            age = today.year - birth_date.year
            return age
        except Exception:
            logger.warning(f"Invalid date_of_birth value: {date_of_birth}")
            return 0

    def _build_prompt(
        self, patient_name: str, date_of_birth: str, notes: list[dict]
    ) -> str:
        """Build the prompt for LLM."""
        age = self._calculate_age(date_of_birth)

        notes_text = "\n\n".join(
            [
                f"Note {i+1} ({note['timestamp']}):\n{note['content']}"
                for i, note in enumerate(notes)
            ]
        )

        prompt = PATIENT_NOTES_SUMMARY_PROMPT.format(
            patient_name=patient_name,
            age=age,
            date_of_birth=date_of_birth,
            notes_text=notes_text,
        )

        return prompt

    async def generate_patient_summary(
        self, patient_name: str, date_of_birth: str, notes: list[dict]
    ) -> str:
        """Generate a patient summary from notes."""
        if not notes:
            return "No medical notes available for this patient."

        prompt = self._build_prompt(patient_name, date_of_birth, notes)
        logger.debug(f"Generating summary for patient: {patient_name}")

        try:
            summary = await self.provider.generate_summary(prompt)
            logger.debug("Summary generated successfully")
            return summary
        except Exception as e:
            raise SummaryGenerationError("Failed to generate patient summary") from e
