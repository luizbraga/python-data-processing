from fastapi.testclient import TestClient

from app.models.patients import Patient


class TestPatientsGetRoutes:
    def test_get_all_patients(self, client: TestClient) -> None:
        response = client.get("/patients/")
        assert response.status_code == 200
        assert isinstance(response.json(), list)

    def test_get_patient_by_id(
        self, client: TestClient, sample_patient: Patient
    ) -> None:
        response = client.get(f"/patients/{sample_patient.id}")
        assert response.status_code == 200
        assert response.json()["id"] == sample_patient.id
        assert response.json()["first_name"] == sample_patient.first_name

    def test_get_patient_not_found(self, client: TestClient) -> None:
        response = client.get("/patients/999999")
        assert response.status_code == 404


class TestPatientsCreateRoutes:

    def test_create_patient(self, client: TestClient) -> None:
        patient_data = {
            "first_name": "John",
            "last_name": "Doe",
            "date_of_birth": "1990-01-15",
            "medical_record_number": "MRN001234",
        }
        response = client.post("/patients/", json=patient_data)
        assert response.status_code == 201
        assert response.json()["first_name"] == patient_data["first_name"]
        assert response.json()["last_name"] == patient_data["last_name"]
        assert response.json()["date_of_birth"] == patient_data["date_of_birth"]
        assert "id" in response.json()

    def test_create_patient_invalid_data(self, client: TestClient) -> None:
        invalid_data = {
            "first_name": "",
            "last_name": "",
            "date_of_birth": "invalid-date",
            "medical_record_number": "",
        }
        response = client.post("/patients/", json=invalid_data)
        assert response.status_code == 422


class TestPatientsUpdateRoutes:
    def test_update_patient(self, client: TestClient, sample_patient: Patient) -> None:
        patient_id = sample_patient.id

        updated_data = {
            "first_name": "Bob",
            "last_name": "Smith Jr.",
            "date_of_birth": "1983-04-12",
            "medical_record_number": "MRN001236",
        }
        response = client.put(f"/patients/{patient_id}", json=updated_data)
        assert response.status_code == 200
        assert response.json()["first_name"] == updated_data["first_name"]
        assert response.json()["last_name"] == updated_data["last_name"]

    def test_update_patient_not_found(self, client: TestClient) -> None:
        updated_data = {
            "first_name": "Non Existent",
            "last_name": "Person",
            "date_of_birth": "1970-01-01",
            "medical_record_number": "MRN000000",
        }
        response = client.put("/patients/999999", json=updated_data)
        assert response.status_code == 404


class TestPatientsDeleteRoutes:

    def test_delete_patient(self, client: TestClient, sample_patient: Patient) -> None:
        patient_id = sample_patient.id

        # Delete the patient
        response = client.delete(f"/patients/{patient_id}")
        assert response.status_code == 204

        # Verify deletion
        get_response = client.get(f"/patients/{patient_id}")
        assert get_response.status_code == 404

    def test_delete_patient_not_found(self, client: TestClient) -> None:
        response = client.delete("/patients/999999")
        assert response.status_code == 404
