from datetime import datetime
from unittest.mock import AsyncMock, MagicMock

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.seed import clear_database, seed_database
from app.models.notes import PatientNote
from app.models.patients import Patient

"""Tests for database seeding utilities."""


@pytest.fixture
def mock_session() -> AsyncMock:
    """Create a mock async session."""
    session = AsyncMock(spec=AsyncSession)
    return session


@pytest.fixture
def mock_execute_result() -> MagicMock:
    """Create a mock execute result."""
    result = MagicMock()
    result.scalars.return_value.all.return_value = []
    return result


class TestSeedDatabase:
    """Tests for seed_database function."""

    @pytest.mark.asyncio
    async def test_seed_database_empty_database(
        self, mock_session: AsyncMock, mock_execute_result: MagicMock
    ) -> None:
        """Test seeding an empty database."""
        mock_session.execute.return_value = mock_execute_result

        await seed_database(mock_session, force=False)

        assert mock_session.add.call_count > 0
        assert mock_session.commit.call_count >= 2
        assert mock_session.refresh.call_count > 0

    @pytest.mark.asyncio
    async def test_seed_database_skip_if_data_exists(
        self, mock_session: AsyncMock
    ) -> None:
        """Test that seeding is skipped when data exists and force=False."""
        existing_patient = Patient(name="Existing Patient", date_of_birth="1990-01-01")
        result = MagicMock()
        result.scalars.return_value.all.return_value = [existing_patient]
        mock_session.execute.return_value = result

        await seed_database(mock_session, force=False)

        mock_session.add.assert_not_called()

    @pytest.mark.asyncio
    async def test_seed_database_force_deletes_existing_data(
        self, mock_session: AsyncMock
    ) -> None:
        """Test that force=True deletes existing data before seeding."""
        existing_patient = Patient(name="Existing Patient", date_of_birth="1990-01-01")
        result = MagicMock()
        result.scalars.return_value.all.return_value = [existing_patient]
        mock_session.execute.return_value = result

        await seed_database(mock_session, force=True)

        mock_session.delete.assert_called_with(existing_patient)

    @pytest.mark.asyncio
    async def test_seed_database_creates_five_patients(
        self, mock_session: AsyncMock, mock_execute_result: MagicMock
    ) -> None:
        """Test that exactly 5 patients are created."""
        mock_session.execute.return_value = mock_execute_result

        await seed_database(mock_session, force=False)

        # 5 patients should be added
        patient_adds = [
            call
            for call in mock_session.add.call_args_list
            if isinstance(call[0][0], Patient)
        ]
        assert len(patient_adds) == 5

    @pytest.mark.asyncio
    async def test_seed_database_creates_notes_for_patients(
        self, mock_session: AsyncMock, mock_execute_result: MagicMock
    ) -> None:
        """Test that notes are created for each patient."""
        # Mock patients with IDs
        mock_patients = []
        for i in range(5):
            patient = MagicMock(spec=Patient)
            patient.id = i + 1
            mock_patients.append(patient)

        mock_session.execute.return_value = mock_execute_result

        await seed_database(mock_session, force=False)

    @pytest.mark.asyncio
    async def test_seed_database_commits_twice(
        self, mock_session: AsyncMock, mock_execute_result: MagicMock
    ) -> None:
        """Test that database commits twice (once for patients, once for notes)."""
        mock_session.execute.return_value = mock_execute_result

        await seed_database(mock_session, force=False)

        assert mock_session.commit.call_count == 2

    @pytest.mark.asyncio
    async def test_seed_database_refreshes_patients(
        self, mock_session: AsyncMock, mock_execute_result: MagicMock
    ) -> None:
        """Test that patients are refreshed to get IDs."""
        mock_session.execute.return_value = mock_execute_result

        await seed_database(mock_session, force=False)

        # Should refresh 5 patients
        assert mock_session.refresh.call_count == 5


class TestClearDatabase:
    """Tests for clear_database function."""

    @pytest.mark.asyncio
    async def test_clear_database_empty(self, mock_session: AsyncMock) -> None:
        """Test clearing an empty database."""
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = result

        await clear_database(mock_session)

        mock_session.delete.assert_not_called()
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_clear_database_deletes_notes_first(
        self, mock_session: AsyncMock
    ) -> None:
        """Test that notes are deleted before patients."""
        note = PatientNote(patient_id=1, content="Test", timestamp=datetime.now())
        patient = Patient(name="Test", date_of_birth="1990-01-01")

        notes_result = MagicMock()
        notes_result.scalars.return_value.all.return_value = [note]

        patients_result = MagicMock()
        patients_result.scalars.return_value.all.return_value = [patient]

        mock_session.execute.side_effect = [notes_result, patients_result]

        await clear_database(mock_session)

        delete_calls = mock_session.delete.call_args_list
        assert len(delete_calls) == 2
        assert isinstance(delete_calls[0][0][0], PatientNote)
        assert isinstance(delete_calls[1][0][0], Patient)

    @pytest.mark.asyncio
    async def test_clear_database_commits_once(self, mock_session: AsyncMock) -> None:
        """Test that database commits once after deleting all data."""
        result = MagicMock()
        result.scalars.return_value.all.return_value = []
        mock_session.execute.return_value = result

        await clear_database(mock_session)

        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_clear_database_deletes_multiple_records(
        self, mock_session: AsyncMock
    ) -> None:
        """Test clearing database with multiple patients and notes."""
        notes = [
            PatientNote(patient_id=1, content="Note 1", timestamp=datetime.now()),
            PatientNote(patient_id=2, content="Note 2", timestamp=datetime.now()),
        ]
        patients = [
            Patient(name="Patient 1", date_of_birth="1990-01-01"),
            Patient(name="Patient 2", date_of_birth="1991-02-02"),
        ]

        notes_result = MagicMock()
        notes_result.scalars.return_value.all.return_value = notes

        patients_result = MagicMock()
        patients_result.scalars.return_value.all.return_value = patients

        mock_session.execute.side_effect = [notes_result, patients_result]

        await clear_database(mock_session)

        assert mock_session.delete.call_count == 4  # 2 notes + 2 patients
