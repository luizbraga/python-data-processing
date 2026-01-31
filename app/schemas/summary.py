from pydantic import BaseModel, Field


class PatientHeading(BaseModel):
    """Patient heading information."""

    patient_id: int = Field(description="Patient's unique identifier")
    name: str = Field(description="Patient's full name")
    date_of_birth: str = Field(description="Patient's date of birth (YYYY-MM-DD)")
    total_notes: int = Field(description="Total number of notes for this patient")


class PatientSummary(BaseModel):
    """Complete patient summary."""

    heading: PatientHeading = Field(description="Patient demographic information")
    summary: str = Field(description="AI-generated narrative summary")
    generated_at: str = Field(description="Timestamp when summary was generated")
