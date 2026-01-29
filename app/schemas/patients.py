from pydantic import BaseModel, ConfigDict, Field


class PatientRead(BaseModel):
    """Pydantic model for reading patient data."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    date_of_birth: str


class PatientCreate(BaseModel):
    """Pydantic model for creating a new patient."""

    name: str = Field(min_length=1, max_length=100)
    date_of_birth: str = Field(pattern=r"^\d{4}-\d{2}-\d{2}$")  # YYYY-MM-DD format


class PatientUpdate(BaseModel):
    """Pydantic model for updating patient data."""

    name: str | None = Field(default=None, min_length=1, max_length=100)
    date_of_birth: str | None = Field(
        default=None, pattern=r"^\d{4}-\d{2}-\d{2}$"
    )  # YYYY-MM-DD format
