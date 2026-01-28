from pydantic import BaseModel, ConfigDict, Field, field_validator


class PatientRead(BaseModel):
    """Pydantic model for reading patient data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    first_name: str
    last_name: str
    date_of_birth: str
    medical_record_number: str


class PatientCreate(BaseModel):
    """Pydantic model for creating a new patient."""

    first_name: str = Field(min_length=1, max_length=50)
    last_name: str = Field(min_length=1, max_length=50)
    date_of_birth: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD format
    medical_record_number: str = Field(min_length=1, max_length=20)


class PatientUpdate(BaseModel):
    """Pydantic model for updating patient data."""

    first_name: str | None = Field(default=None, min_length=1, max_length=50)
    last_name: str | None = Field(default=None, min_length=1, max_length=50)
    date_of_birth: str | None = Field(
        default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"
    )  # YYYY-MM-DD format
    medical_record_number: str | None = Field(default=None, min_length=1, max_length=20)
