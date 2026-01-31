"""Database seeding utilities for development/demo environments."""

import logging
from datetime import datetime, timedelta

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.notes import PatientNote
from app.models.patients import Patient

logger = logging.getLogger(__name__)


async def seed_database(session: AsyncSession, force: bool = False) -> None:
    """Seed the database with sample data.

    Args:
        session: Database session
        force: If True, delete existing data and reseed
    """
    # Check if data already exists
    result = await session.execute(select(Patient))
    existing_patients = result.scalars().all()

    if existing_patients and not force:
        logger.info("Database already contains data. Skipping seed.")
        return

    if force and existing_patients:
        logger.warning("Force flag set. Deleting existing data...")
        for patient in existing_patients:
            await session.delete(patient)
        await session.commit()

    logger.info("Seeding database with sample data...")

    # Create sample patients
    patients_data = [
        {
            "name": "John Doe",
            "date_of_birth": "1985-03-15",
        },
        {
            "name": "Jane Smith",
            "date_of_birth": "1990-07-22",
        },
        {
            "name": "Robert Johnson",
            "date_of_birth": "1978-11-30",
        },
        {
            "name": "Maria Garcia",
            "date_of_birth": "1995-05-18",
        },
        {
            "name": "Michael Brown",
            "date_of_birth": "1982-09-08",
        },
    ]

    patients = []
    for data in patients_data:
        patient = Patient(**data)
        session.add(patient)
        patients.append(patient)

    await session.commit()

    # Refresh to get IDs
    for patient in patients:
        await session.refresh(patient)

    logger.info(f"Created {len(patients)} patients")

    # Create sample notes for each patient
    base_time = datetime.now() - timedelta(days=30)

    notes_data = [
        # John Doe - Hypertension case
        {
            "patient": patients[0],
            "notes": [
                (
                    "Initial Consultation: Patient presents with elevated blood pressure (145/95). "
                    "Reports occasional headaches and family history of hypertension. "
                    "No chest pain or shortness of breath. Started on Lisinopril 10mg daily.",
                    base_time,
                ),
                (
                    "Follow-up (Week 2): Blood pressure improved to 135/88. "
                    "Patient tolerating medication well. Continue current dose.",
                    base_time + timedelta(days=14),
                ),
                (
                    "Follow-up (Month 1): Blood pressure now 128/82. Excellent response to treatment. "
                    "Patient reports no adverse effects. Recommend continue medication and follow up in 3 months.",
                    base_time + timedelta(days=30),
                ),
            ],
        },
        # Jane Smith - Diabetes management
        {
            "patient": patients[1],
            "notes": [
                (
                    "New Patient Visit: 32-year-old female with newly diagnosed Type 2 Diabetes. "
                    "HbA1c 8.2%. BMI 31. Started on Metformin 500mg BID. "
                    "Discussed lifestyle modifications and dietary changes.",
                    base_time + timedelta(days=1),
                ),
                (
                    "Follow-up (Week 3): Blood glucose levels improving. Fasting glucose down from 165 to 140. "
                    "Patient reports better energy levels. Increased Metformin to 1000mg BID.",
                    base_time + timedelta(days=21),
                ),
                (
                    "Lab Review: HbA1c down to 7.1%. Continue current regimen. "
                    "Patient motivated and compliant with diet and exercise program.",
                    base_time + timedelta(days=28),
                ),
            ],
        },
        # Robert Johnson - Routine checkup
        {
            "patient": patients[2],
            "notes": [
                (
                    "Annual Physical: 47-year-old male in good health. "
                    "Vital signs normal. No significant complaints. "
                    "Labs ordered: CBC, CMP, lipid panel. Recommended colonoscopy screening.",
                    base_time + timedelta(days=2),
                ),
                (
                    "Lab Results Review: All labs within normal limits. Cholesterol slightly elevated (220). "
                    "Discussed dietary modifications. No medication needed at this time.",
                    base_time + timedelta(days=9),
                ),
            ],
        },
        # Maria Garcia - Prenatal care
        {
            "patient": patients[3],
            "notes": [
                (
                    "Initial Prenatal Visit: 28-year-old G1P0 at 8 weeks gestation. "
                    "Prenatal labs ordered. Started on prenatal vitamins. "
                    "Next visit scheduled for 12 weeks with ultrasound.",
                    base_time + timedelta(days=5),
                ),
                (
                    "12-Week Checkup: Ultrasound shows single viable intrauterine pregnancy. "
                    "EDD confirmed. Nuchal translucency normal. Patient feeling well, minimal nausea.",
                    base_time + timedelta(days=33),
                ),
            ],
        },
        # Michael Brown - Post-surgical follow-up
        {
            "patient": patients[4],
            "notes": [
                (
                    "Post-Op Day 7: S/P appendectomy. Wound healing well, no signs of infection. "
                    "Pain controlled with ibuprofen. Cleared to return to light activities.",
                    base_time + timedelta(days=7),
                ),
                (
                    "2-Week Follow-up: Excellent recovery. No complications. "
                    "Wound completely healed. Cleared for normal activities.",
                    base_time + timedelta(days=14),
                ),
            ],
        },
    ]

    total_notes = 0
    for patient_notes in notes_data:
        patient_id = getattr(patient_notes["patient"], "id")
        if not patient_id:
            continue
        note_list: list[tuple[str, datetime]] = patient_notes["notes"]  # type: ignore

        for content, timestamp in note_list:
            note = PatientNote(
                patient_id=patient_id,
                content=content,
                timestamp=timestamp,
            )
            session.add(note)
            total_notes += 1

    await session.commit()
    logger.info(f"Created {total_notes} notes across {len(patients)} patients")
    logger.info("Database seeding completed successfully!")


async def clear_database(session: AsyncSession) -> None:
    """Clear all data from the database.

    Args:
        session: Database session
    """
    logger.warning("Clearing all data from database...")

    # Delete all notes first (due to foreign key)
    result = await session.execute(select(PatientNote))
    notes = list(result.scalars().all())
    for note in notes:
        await session.delete(note)

    # Delete all patients
    result = await session.execute(select(Patient))
    patients_list: list[Patient] = list(result.scalars().all())
    for patient in patients_list:
        await session.delete(patient)

    await session.commit()
    logger.info("Database cleared successfully!")
