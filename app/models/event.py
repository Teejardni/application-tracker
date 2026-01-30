from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any

from app.models.enums import EventType


class EventCreate(BaseModel):
    event_type: EventType
    event_date: datetime
    metadata: Optional[Dict[str, Any]] = None


class EventRead(BaseModel):
    id: int
    application_id: int
    event_type: EventType
    event_date: datetime
    metadata: Optional[Dict[str, Any]]

    class Config:
        from_attributes = True

