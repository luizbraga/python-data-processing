"""Main FastAPI application."""

from typing import Any

from fastapi import Depends, FastAPI, HTTPException
from pydantic import BaseModel, ConfigDict, Field
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.models import Item

app = FastAPI(title=settings.app_name, debug=settings.debug)


class ItemCreate(BaseModel):
    """Pydantic model for creating an item."""

    name: str = Field(..., min_length=1, max_length=100)
    description: str | None = Field(None, max_length=500)


class ItemResponse(BaseModel):
    """Pydantic model for item response."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    description: str | None = None


@app.get("/")
def read_root() -> dict[str, str]:
    """Root endpoint."""
    return {"message": "Welcome to Python Data Processing API"}


@app.get("/health")
def health_check() -> dict[str, str]:
    """Health check endpoint."""
    return {"status": "ok"}


@app.get("/items", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)) -> Any:
    """Get all items."""
    try:
        items = db.query(Item).all()
        return items
    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail="Database error occurred")


@app.post("/items", response_model=ItemResponse, status_code=201)
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Any:
    """Create a new item."""
    try:
        db_item = Item(name=item.name, description=item.description)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail="Failed to create item")
