from datetime import datetime
from typing import Generator
from unittest.mock import AsyncMock, MagicMock, patch

import pytest

from app.llm.exceptions import SummaryGenerationError
from app.llm.prompts import PATIENT_NOTES_SUMMARY_PROMPT
from app.llm.service import LLMService


@pytest.fixture
def mock_llm_service() -> Generator[MagicMock, None, None]:
    with patch("app.llm.service.LLMService._get_provider") as mock_get_provider:
        yield mock_get_provider


class TestLLMService:
    def test_initialization(self) -> None:
        with patch(
            "app.llm.service.LLMService._get_provider", return_value="some_provider"
        ) as mock_get_provider:
            service = LLMService()
            mock_get_provider.assert_called_once()
            assert service.provider == mock_get_provider.return_value

    def test_get_provider(self) -> None:
        with (
            patch(
                "app.llm.service.OpenAIProvider", return_value="some_provider"
            ) as mock_provider,
            patch("app.config.settings.llm_provider", "openai"),
        ):
            service = LLMService()
            provider = service.provider
            assert isinstance(provider, mock_provider.return_value.__class__)
            mock_provider.assert_called_once()

    def test_get_provider_unknown(self) -> None:
        with patch("app.config.settings.llm_provider", "unknown"):
            with pytest.raises(ValueError, match="Unknown LLM provider: unknown"):
                LLMService()

    def test_calculate_age(self) -> None:
        service = LLMService()
        age = service._calculate_age("2000-01-01")
        today = datetime.now()
        assert isinstance(age, int)
        assert age == today.year - 2000

    def test_build_prompt(self) -> None:
        service = LLMService()
        notes = [
            {"timestamp": "2023-10-01", "content": "Patient is recovering well."},
            {"timestamp": "2023-10-15", "content": "No signs of infection."},
        ]
        prompt = service._build_prompt("John Doe", "1990-05-20", notes)

        assert prompt == PATIENT_NOTES_SUMMARY_PROMPT.format(
            patient_name="John Doe",
            age=service._calculate_age("1990-05-20"),
            date_of_birth="1990-05-20",
            notes_text=f"Note 1 ({notes[0]['timestamp']}):\n{notes[0]['content']}\n\nNote 2 ({notes[1]['timestamp']}):\n{notes[1]['content']}",
        )

    def test_build_prompt_no_notes(self) -> None:
        service = LLMService()
        prompt = service._build_prompt("Jane Doe", "1985-12-10", [])

        assert prompt == PATIENT_NOTES_SUMMARY_PROMPT.format(
            patient_name="Jane Doe",
            age=service._calculate_age("1985-12-10"),
            date_of_birth="1985-12-10",
            notes_text="",
        )

    @pytest.mark.asyncio
    async def test_generate_patient_summary_no_notes(
        self, mock_llm_service: Generator[MagicMock, None, None]
    ) -> None:
        assert isinstance(mock_llm_service, MagicMock)
        service = LLMService()
        summary = await service.generate_patient_summary("John Doe", "1990-01-01", [])
        assert summary == "No medical notes available for this patient."
        mock_llm_service.return_value.assert_not_called()

    @pytest.mark.asyncio
    async def test_generate_patient_summary_with_notes(
        self, mock_llm_service: Generator[MagicMock, None, None]
    ) -> None:
        assert isinstance(mock_llm_service, MagicMock)
        mock_llm_service.return_value.generate_summary = AsyncMock(
            return_value="Generated summary"
        )
        service = LLMService()
        notes = [
            {"timestamp": "2023-10-01", "content": "Patient is recovering well."},
        ]
        summary = await service.generate_patient_summary(
            "John Doe", "1990-05-20", notes
        )
        assert summary == "Generated summary"
        mock_llm_service.return_value.generate_summary.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_generate_patient_summary_llm_error(
        self, mock_llm_service: Generator[MagicMock, None, None]
    ) -> None:
        assert isinstance(mock_llm_service, MagicMock)
        mock_llm_service.return_value.generate_summary = AsyncMock(
            side_effect=Exception("LLM error")
        )
        service = LLMService()
        notes = [
            {"timestamp": "2023-10-01", "content": "Patient is recovering well."},
        ]
        with pytest.raises(
            SummaryGenerationError, match="Failed to generate patient summary"
        ) as exc:
            await service.generate_patient_summary("John Doe", "1990-05-20", notes)
            exc_info = exc.value.__cause__
            assert str(exc_info) == "LLM error"
        mock_llm_service.return_value.generate_summary.assert_awaited_once()
