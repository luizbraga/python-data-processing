from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PatientRead(BaseModel):
    """Pydantic model for reading patient data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date_of_birth: str


class PatientBase(BaseModel):
    """Base model with shared validators."""

    @field_validator("date_of_birth", check_fields=False)
    @classmethod
    def validate_date_of_birth(cls, value: str | None) -> str | None:
        if value is None:
            return value
        year, month, day = map(int, value.split("-"))
        current_year = datetime.now().year
        if not (1 <= month <= 12):
            raise ValueError("Month must be between 1 and 12")
        if not (1 <= day <= 31):
            raise ValueError("Day must be between 1 and 31")
        if year < 1900 or year > current_year:
            raise ValueError(f"Year must be between 1900 and {current_year}")
        return value

    @field_validator("name", check_fields=False)
    @classmethod
    def validate_name(cls, value: str | None) -> str | None:
        if value is None:
            return value
        if not value.strip():
            raise ValueError("Name cannot be empty or whitespace")
        return " ".join(value.strip().split())  # Normalize whitespace


class PatientCreate(PatientBase):
    """Pydantic model for creating a new patient."""

    name: str = Field(min_length=1, max_length=100)
    date_of_birth: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD format


class PatientUpdate(PatientBase):
    """Pydantic model for updating patient data."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    date_of_birth: str | None = Field(
        default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"
    )  # YYYY-MM-DD format
