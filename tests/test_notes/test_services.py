from datetime import datetime, timezone

import pytest
from fastapi_pagination import Params, set_params
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.patients import Patient
from app.services.notes import NoteService

pytestmark = pytest.mark.asyncio


async def test_create_note(db_session: AsyncSession, sample_patient: Patient) -> None:
    service = NoteService(db_session)
    note = await service.create_note(
        patient_id=sample_patient.id,
        content="Patient doing well",
        timestamp=datetime.now(),
    )
    assert note.id is not None
    assert note.patient_id == sample_patient.id
    assert note.content == "Patient doing well"


async def test_get_patient_notes(
    db_session: AsyncSession, sample_patient: Patient
) -> None:
    set_params(Params(size=10, page=1))
    service = NoteService(db_session)
    # Create multiple notes
    for i in range(5):
        await service.create_note(
            patient_id=sample_patient.id,
            content=f"Note {i}",
            timestamp=datetime.now(),
        )

    notes = await service.get_patient_notes(patient_id=sample_patient.id)
    assert len(notes.items) == 5
    assert all(note.patient_id == sample_patient.id for note in notes.items)


async def test_get_note_by_id(
    db_session: AsyncSession, sample_patient: Patient
) -> None:
    service = NoteService(db_session)
    note = await service.create_note(
        patient_id=sample_patient.id,
        content="Specific note",
        timestamp=datetime.now(),
    )

    fetched_note = await service.get_note(note_id=note.id)
    assert fetched_note is not None
    assert fetched_note.id == note.id
    assert fetched_note.content == "Specific note"


async def test_create_note_invalid_patient(db_session: AsyncSession) -> None:
    service = NoteService(db_session)
    try:
        await service.create_note(
            patient_id=9999,  # Non-existent patient ID
            content="This should fail",
            timestamp=datetime.now(),
        )
    except ValueError as e:
        assert str(e) == "Patient with id 9999 not found"


async def test_get_patient_notes_sorted(
    db_session: AsyncSession, sample_patient: Patient
) -> None:
    set_params(Params(size=10, page=1))
    service = NoteService(db_session)
    # Create notes with different timestamps
    timestamps = [
        datetime(2023, 1, 1, 10, 0, tzinfo=timezone.utc),
        datetime(2023, 1, 2, 10, 0, tzinfo=timezone.utc),
        datetime(2023, 1, 3, 10, 0, tzinfo=timezone.utc),
    ]
    for i, ts in enumerate(timestamps):
        await service.create_note(
            patient_id=sample_patient.id,
            content=f"Note {i}",
            timestamp=ts,
        )

    # Fetch notes sorted by timestamp ascending
    notes_asc = await service.get_patient_notes(
        patient_id=sample_patient.id, sort_by="timestamp"
    )
    assert [note.timestamp for note in notes_asc.items] == sorted(timestamps)

    # Fetch notes sorted by timestamp descending
    notes_desc = await service.get_patient_notes(
        patient_id=sample_patient.id, sort_by="-timestamp"
    )
    assert [note.timestamp for note in notes_desc.items] == sorted(
        timestamps, reverse=True
    )


async def test_delete_note(db_session: AsyncSession, sample_patient: Patient) -> None:
    service = NoteService(db_session)
    note = await service.create_note(
        patient_id=sample_patient.id,
        content="Note to be deleted",
        timestamp=datetime.now(),
    )

    deleted = await service.delete_note(note_id=note.id)
    assert deleted is True

    fetched_note = await service.get_note(note_id=note.id)
    assert fetched_note is None


async def test_delete_nonexistent_note(db_session: AsyncSession) -> None:
    service = NoteService(db_session)
    deleted = await service.delete_note(note_id=9999)  # Non-existent note ID
    assert deleted is False


async def test_delete_patient_notes(
    db_session: AsyncSession, sample_patient: Patient
) -> None:
    set_params(Params(size=10, page=1))
    service = NoteService(db_session)
    # Create multiple notes
    for i in range(3):
        await service.create_note(
            patient_id=sample_patient.id,
            content=f"Note {i}",
            timestamp=datetime.now(),
        )

    deleted_count = await service.delete_patient_notes(patient_id=sample_patient.id)
    assert deleted_count == 3

    notes = await service.get_patient_notes(patient_id=sample_patient.id)
    assert len(notes.items) == 0


async def test_get_all_patient_notes(
    db_session: AsyncSession, sample_patient: Patient
) -> None:
    service = NoteService(db_session)
    # Create multiple notes
    for i in range(4):
        await service.create_note(
            patient_id=sample_patient.id,
            content=f"Note {i}",
            timestamp=datetime.now(),
        )

    notes = await service.get_all_patient_notes(patient_id=sample_patient.id)
    assert len(notes) == 4
    assert all(note.patient_id == sample_patient.id for note in notes)
