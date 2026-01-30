from datetime import datetime
from unittest.mock import Mock

import pytest
from fastapi_pagination import Params, set_params
from httpx import AsyncClient

pytestmark = pytest.mark.asyncio


class TestCreateNoteFileRoute:
    async def test_create_note_file(
        self, client_with_mock_note_service: AsyncClient, mock_service: Mock
    ) -> None:
        patient_id = 1
        mock_service.create_note.return_value = {
            "id": 1,
            "patient_id": patient_id,
            "content": "Sample note content",
            "created_at": "2024-01-01T12:00:00",
            "timestamp": "2024-01-01T12:00:00",
        }
        files = {
            "file": ("note.txt", b"Sample note content", "text/plain"),
        }
        data = {
            "timestamp": "2024-01-01T12:00:00",
        }
        response = await client_with_mock_note_service.post(
            f"/patients/{patient_id}/notes/upload", files=files, data=data
        )
        assert response.status_code == 201
        assert response.json()["content"] == "Sample note content"
        mock_service.create_note.assert_awaited_once_with(
            patient_id=patient_id,
            content="Sample note content",
            timestamp=datetime(2024, 1, 1, 12, 0),
        )


class TestGetPatientNoteRoute:
    async def test_get_patient_note(
        self, client_with_mock_note_service: AsyncClient, mock_service: Mock
    ) -> None:
        patient_id = 1
        note_id = 1
        mock_service.get_note.return_value = {
            "id": note_id,
            "patient_id": patient_id,
            "content": "Sample note content",
            "created_at": "2024-01-01T12:00:00",
            "timestamp": "2024-01-01T12:00:00",
        }
        response = await client_with_mock_note_service.get(
            f"/patients/{patient_id}/notes/{note_id}"
        )
        assert response.status_code == 200
        assert response.json()["id"] == note_id
        mock_service.get_note.assert_awaited_once_with(note_id)


class TestListPatientsNotesRoute:
    async def test_list_patient_notes(
        self, client_with_mock_note_service: AsyncClient, mock_service: Mock
    ) -> None:
        set_params(Params(size=10, page=1))
        patient_id = 1
        mock_service.get_patient_notes.return_value = {
            "items": [
                {
                    "id": 1,
                    "patient_id": patient_id,
                    "content": "Note 1",
                    "created_at": "2024-01-01T12:00:00",
                    "timestamp": "2024-01-01T12:00:00",
                },
                {
                    "id": 2,
                    "patient_id": patient_id,
                    "content": "Note 2",
                    "created_at": "2024-01-02T12:00:00",
                    "timestamp": "2024-01-02T12:00:00",
                },
            ],
            "total": 2,
            "page": 1,
            "size": 50,
            "pages": 1,
        }
        response = await client_with_mock_note_service.get(
            f"/patients/{patient_id}/notes/"
        )
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        mock_service.get_patient_notes.assert_awaited_once_with(patient_id, None)


class TestDeletePatientNoteRoute:
    async def test_delete_patient_note(
        self, client_with_mock_note_service: AsyncClient, mock_service: Mock
    ) -> None:
        patient_id = 1
        note_id = 1
        mock_service.get_note.return_value = {
            "id": note_id,
            "patient_id": patient_id,
            "content": "Sample note content",
            "created_at": "2024-01-01T12:00:00",
            "timestamp": "2024-01-01T12:00:00",
        }
        response = await client_with_mock_note_service.delete(
            f"/patients/{patient_id}/notes/{note_id}"
        )
        assert response.status_code == 204
        mock_service.get_note.assert_awaited_once_with(note_id)
        mock_service.delete_note.assert_awaited_once_with(note_id)
