"""Main FastAPI application."""

from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from typing import Any
from pydantic import BaseModel, ConfigDict

from app.config import settings
from app.database import get_db

app = FastAPI(title=settings.app_name, debug=settings.debug)


class ItemCreate(BaseModel):
    """Pydantic model for creating an item."""

    name: str
    description: str | None = None


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
    return {"status": "healthy"}


@app.get("/items", response_model=list[ItemResponse])
def get_items(db: Session = Depends(get_db)) -> Any:
    """Get all items."""
    from app.models import Item

    items = db.query(Item).all()
    return items


@app.post("/items", response_model=ItemResponse)
def create_item(item: ItemCreate, db: Session = Depends(get_db)) -> Any:
    """Create a new item."""
    from app.models import Item

    db_item = Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
