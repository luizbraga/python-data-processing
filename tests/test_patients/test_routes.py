from unittest.mock import Mock

from fastapi.testclient import TestClient

from app.models.patients import Patient


class TestPatientsGetRoutes:
    def test_get_all_patients(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        mock_patient_service.list_patients.return_value = {
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
        response = client_with_mock_service.get("/patients/")
        assert response.status_code == 200
        assert isinstance(response.json(), dict)
        mock_patient_service.list_patients.assert_called_once()

    def test_get_patient_by_id(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        patient = Patient(
            id=1,
            name="John Doe",
            date_of_birth="1990-01-15",
        )
        mock_patient_service.get_patient.return_value = patient
        response = client_with_mock_service.get(f"/patients/{patient.id}")

        mock_patient_service.get_patient.assert_called_once_with(patient.id)
        assert response.status_code == 200
        assert response.json()["id"] == patient.id
        assert response.json()["name"] == patient.name

    def test_get_patient_not_found(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        mock_patient_service.get_patient.return_value = None
        response = client_with_mock_service.get("/patients/999999")
        mock_patient_service.get_patient.assert_called_once_with(999999)
        assert response.status_code == 404


class TestPatientsCreateRoutes:

    def test_create_patient(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        patient_data = {
            "name": "John Doe",
            "date_of_birth": "1990-01-15",
        }
        mock_patient_service.create_patient.return_value = Patient(id=1, **patient_data)
        response = client_with_mock_service.post("/patients/", json=patient_data)
        mock_patient_service.create_patient.assert_called_once_with(patient_data)
        assert response.status_code == 201
        assert (
            response.json()["id"] == mock_patient_service.create_patient.return_value.id
        )
        assert response.json()["name"] == patient_data["name"]
        assert response.json()["date_of_birth"] == patient_data["date_of_birth"]

    def test_create_patient_invalid_data(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        invalid_data = {
            "name": "",
            "date_of_birth": "invalid-date",
        }
        response = client_with_mock_service.post("/patients/", json=invalid_data)
        mock_patient_service.create_patient.assert_not_called()
        assert response.status_code == 422

    def test_create_patient_normalize_empty_spaces_in_name(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        patient_data = {
            "name": "   John    Doe   ",
            "date_of_birth": "1990-01-15",
        }
        normalized_name = "John Doe"
        mock_patient_service.create_patient.return_value = Patient(
            id=1, name=normalized_name, date_of_birth=patient_data["date_of_birth"]
        )
        response = client_with_mock_service.post("/patients/", json=patient_data)
        mock_patient_service.create_patient.assert_called_once_with(
            {
                "name": normalized_name,
                "date_of_birth": patient_data["date_of_birth"],
            }
        )
        assert response.status_code == 201
        assert response.json()["name"] == normalized_name

    def test_create_patient_invalid_date_value(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        invalid_data = {
            "name": "John Doe",
            "date_of_birth": "1990-12-99",  # Invalid date
        }
        response = client_with_mock_service.post("/patients/", json=invalid_data)
        mock_patient_service.create_patient.assert_not_called()
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Day must be between 1 and 31"
        )

    def test_create_patient_invalid_month_value(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        invalid_data = {
            "name": "John Doe",
            "date_of_birth": "1990-99-30",  # Invalid date
        }
        response = client_with_mock_service.post("/patients/", json=invalid_data)
        mock_patient_service.create_patient.assert_not_called()
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Month must be between 1 and 12"
        )

    def test_create_patient_invalid_year_value(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        invalid_data = {
            "name": "John Doe",
            "date_of_birth": "1800-12-30",  # Invalid date
        }
        response = client_with_mock_service.post("/patients/", json=invalid_data)
        mock_patient_service.create_patient.assert_not_called()
        assert response.status_code == 422
        assert (
            response.json()["detail"][0]["msg"]
            == "Value error, Year must be between 1900 and 2026"
        )


class TestPatientsUpdateRoutes:
    def test_update_patient(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        patient_id = 1

        updated_data = {
            "name": "Bob Smith Jr.",
            "date_of_birth": "1983-04-12",
        }
        mock_patient_service.update_patient.return_value = Patient(
            id=patient_id, **updated_data
        )
        response = client_with_mock_service.put(
            f"/patients/{patient_id}", json=updated_data
        )
        mock_patient_service.update_patient.assert_called_once_with(
            patient_id, updated_data
        )
        assert response.status_code == 200
        assert response.json()["name"] == updated_data["name"]

    def test_update_patient_not_found(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        updated_data = {
            "name": "Non Existent",
            "date_of_birth": "1970-01-01",
        }
        mock_patient_service.update_patient.return_value = None
        response = client_with_mock_service.put("/patients/999999", json=updated_data)
        mock_patient_service.update_patient.assert_called_once_with(
            999999, updated_data
        )
        assert response.status_code == 404


class TestPatientsDeleteRoutes:

    def test_delete_patient(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        patient_id = 1
        mock_patient_service.delete_patient.return_value = True
        mock_patient_service.get_patient.return_value = None

        # Delete the patient
        response = client_with_mock_service.delete(f"/patients/{patient_id}")
        mock_patient_service.delete_patient.assert_called_once_with(patient_id)
        assert response.status_code == 204

        # Verify deletion
        get_response = client_with_mock_service.get(f"/patients/{patient_id}")
        mock_patient_service.get_patient.assert_called_with(patient_id)
        assert get_response.status_code == 404

    def test_delete_patient_not_found(
        self, client_with_mock_service: TestClient, mock_patient_service: Mock
    ) -> None:
        mock_patient_service.delete_patient.return_value = False
        response = client_with_mock_service.delete("/patients/999999")
        mock_patient_service.delete_patient.assert_called_once_with(999999)
        assert response.status_code == 404
