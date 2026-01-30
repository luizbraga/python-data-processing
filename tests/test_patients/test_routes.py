from unittest.mock import Mock

import pytest
from httpx import AsyncClient

from app.models.patients import Patient

pytestmark = pytest.mark.asyncio


class TestPatientsGetRoutes:
    async def test_get_all_patients(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        mock_service.list_patients.return_value = {
            "items": [
                Patient(
                    id=1,
                    name="John Doe",
                    date_of_birth="1990-01-15",
                ),
                Patient(
                    id=2,
                    name="Jane Smith",
                    date_of_birth="1985-07-30",
                ),
                Patient(
                    id=3,
                    name="Alice Johnson",
                    date_of_birth="1978-11-22",
                ),
            ],
            "total": 3,
            "page": 1,
            "size": 50,
            "pages": 1,
        }
        response = await client_with_mock_patient_service.get("/patients/")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        mock_service.list_patients.assert_awaited_once_with(
            sort_by=None, name_filter=None
        )

    async def test_get_patient_by_id(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        patient = Patient(
            id=1,
            name="John Doe",
            date_of_birth="1990-01-15",
        )
        mock_service.get_patient.return_value = patient
        response = await client_with_mock_patient_service.get(f"/patients/{patient.id}")

        mock_service.get_patient.assert_awaited_once_with(patient.id)
        assert response.status_code == 200
        assert response.json()["id"] == patient.id
        assert response.json()["name"] == patient.name

    async def test_get_patient_not_found(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        mock_service.get_patient.return_value = None
        response = await client_with_mock_patient_service.get("/patients/999999")
        mock_service.get_patient.assert_awaited_once_with(999999)
        assert response.status_code == 404


class TestPatientsCreateRoutes:

    async def test_create_patient(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        patient_data = {
            "name": "John Doe",
            "date_of_birth": "1990-01-15",
        }
        mock_service.create_patient.return_value = Patient(id=1, **patient_data)
        response = await client_with_mock_patient_service.post(
            "/patients/", json=patient_data
        )
        mock_service.create_patient.assert_awaited_once_with(patient_data)
        assert response.status_code == 201
        assert response.json()["id"] == mock_service.create_patient.return_value.id
        assert response.json()["name"] == patient_data["name"]
        assert response.json()["date_of_birth"] == patient_data["date_of_birth"]

    async def test_create_patient_invalid_data(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        invalid_data = {
            "name": "",
            "date_of_birth": "invalid-date",
        }
        response = await client_with_mock_patient_service.post(
            "/patients/", json=invalid_data
        )
        mock_service.create_patient.assert_not_called()
        assert response.status_code == 422

    async def test_create_patient_normalize_empty_spaces_in_name(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        patient_data = {
            "name": "   John    Doe   ",
            "date_of_birth": "1990-01-15",
        }
        normalized_name = "John Doe"
        mock_service.create_patient.return_value = Patient(
            id=1, name=normalized_name, date_of_birth=patient_data["date_of_birth"]
        )
        response = await client_with_mock_patient_service.post(
            "/patients/", json=patient_data
        )
        mock_service.create_patient.assert_awaited_once_with(
            {
                "name": normalized_name,
                "date_of_birth": patient_data["date_of_birth"],
            }
        )
        assert response.status_code == 201
        assert response.json()["name"] == normalized_name

    async def test_create_patient_invalid_date_value(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        invalid_data = {
            "name": "John Doe",
            "date_of_birth": "1990-12-99",  # Invalid date
        }
        response = await client_with_mock_patient_service.post(
            "/patients/", json=invalid_data
        )
        mock_service.create_patient.assert_not_called()
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Day must be between 1 and 31"
        )

    async def test_create_patient_invalid_month_value(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        invalid_data = {
            "name": "John Doe",
            "date_of_birth": "1990-99-30",  # Invalid date
        }
        response = await client_with_mock_patient_service.post(
            "/patients/", json=invalid_data
        )
        mock_service.create_patient.assert_not_called()
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Month must be between 1 and 12"
        )

    async def test_create_patient_invalid_year_value(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        invalid_data = {
            "name": "John Doe",
            "date_of_birth": "1800-12-30",  # Invalid date
        }
        response = await client_with_mock_patient_service.post(
            "/patients/", json=invalid_data
        )
        mock_service.create_patient.assert_not_called()
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Year must be between 1900 and 2026"
        )


class TestPatientsUpdateRoutes:
    async def test_update_patient(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        patient_id = 1

        updated_data = {
            "name": "Bob Smith Jr.",
            "date_of_birth": "1983-04-12",
        }
        mock_service.update_patient.return_value = Patient(
            id=patient_id, **updated_data
        )
        response = await client_with_mock_patient_service.put(
            f"/patients/{patient_id}", json=updated_data
        )
        mock_service.update_patient.assert_awaited_once_with(patient_id, updated_data)
        assert response.status_code == 200
        assert response.json()["name"] == updated_data["name"]

    async def test_update_patient_not_found(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        updated_data = {
            "name": "Non Existent",
            "date_of_birth": "1970-01-01",
        }
        mock_service.update_patient.return_value = None
        response = await client_with_mock_patient_service.put(
            "/patients/999999", json=updated_data
        )
        mock_service.update_patient.assert_awaited_once_with(999999, updated_data)
        assert response.status_code == 404


class TestPatientsDeleteRoutes:

    async def test_delete_patient(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        patient_id = 1
        mock_service.delete_patient.return_value = True
        mock_service.get_patient.return_value = None

        # Delete the patient
        response = await client_with_mock_patient_service.delete(
            f"/patients/{patient_id}"
        )
        mock_service.delete_patient.assert_awaited_once_with(patient_id)
        assert response.status_code == 204

        # Verify deletion
        get_response = await client_with_mock_patient_service.get(
            f"/patients/{patient_id}"
        )
        mock_service.get_patient.assert_called_with(patient_id)
        assert get_response.status_code == 404

    async def test_delete_patient_not_found(
        self, client_with_mock_patient_service: AsyncClient, mock_service: Mock
    ) -> None:
        mock_service.delete_patient.return_value = False
        response = await client_with_mock_patient_service.delete("/patients/999999")
        mock_service.delete_patient.assert_awaited_once_with(999999)
        assert response.status_code == 404
