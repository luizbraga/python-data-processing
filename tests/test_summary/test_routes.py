from unittest.mock import AsyncMock

import pytest
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestSummaryRoutes:

    async def test_get_patient_summary(
        self,
        client_with_mock_summary_service: AsyncClient,
        mock_service: AsyncMock,
        mock_llm: AsyncMock,
    ) -> None:
        mock_service.generate_summary.return_value = {
            "heading": {
                "patient_id": 1,
                "name": "John Doe",
                "date_of_birth": "1990-01-15",
                "total_notes": 3,
            },
            "summary": "This is a sample summary.",
            "generated_at": "2024-01-01T12:00:00",
        }

        response = await client_with_mock_summary_service.get("/patients/1/summary")

        assert response.status_code == 200
        data = response.json()
        assert data["heading"]["patient_id"] == 1
        assert data["heading"]["name"] == "John Doe"
        assert data["heading"]["date_of_birth"] == "1990-01-15"
        assert data["heading"]["total_notes"] == 3
        assert data["summary"] == "This is a sample summary."
        assert data["generated_at"] == "2024-01-01T12:00:00"
        mock_service.generate_summary.assert_awaited_once_with(
            patient_id=1, llm_service=mock_llm
        )

    async def test_get_patient_summary_not_found(
        self,
        client_with_mock_summary_service: AsyncClient,
        mock_service: AsyncMock,
        mock_llm: AsyncMock,
    ) -> None:
        mock_service.generate_summary.side_effect = ValueError(
            "Patient with id 999 not found"
        )

        response = await client_with_mock_summary_service.get("/patients/999/summary")

        assert response.status_code == 404
        data = response.json()
        assert data["detail"] == "Patient with id 999 not found"
        mock_service.generate_summary.assert_awaited_once_with(
            patient_id=999, llm_service=mock_llm
        )

    async def test_get_patient_summary_server_error(
        self,
        client_with_mock_summary_service: AsyncClient,
        mock_service: AsyncMock,
        mock_llm: AsyncMock,
    ) -> None:
        mock_service.generate_summary.side_effect = Exception(
            "Database connection error"
        )

        response = await client_with_mock_summary_service.get("/patients/1/summary")

        assert response.status_code == 500
        data = response.json()
        assert data["detail"] == "Failed to generate summary: Database connection error"
        mock_service.generate_summary.assert_awaited_once_with(
            patient_id=1, llm_service=mock_llm
        )
