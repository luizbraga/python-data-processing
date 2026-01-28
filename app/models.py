"""SQLAlchemy models for the application."""
from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime

from app.database import Base


class Item(Base):
    """Example Item model."""

    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
