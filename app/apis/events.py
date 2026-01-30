from fastapi import APIRouter, HTTPException
from typing import List

from app.models.event import EventCreate, EventRead
from app.services.events import add_event, list_events


router = APIRouter(
    prefix="/applications/{app_id}/events",
    tags=["events"],
)


@router.post("", response_model=EventRead)
async def create_event(app_id: int, data: EventCreate):
    try:
        return await add_event(app_id, data)
    except Exception:
        raise HTTPException(status_code=404, detail="Application not found")


@router.get("", response_model=List[EventRead])
async def list_all(app_id: int):
    return await list_events(app_id)

