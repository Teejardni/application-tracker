from fastapi import APIRouter, HTTPException
from typing import List

from app.models.application import (
    ApplicationCreate,
    ApplicationUpdate,
    ApplicationRead,
)
from app.services.applications import (
    create_application,
    update_application,
    get_application,
    list_applications,
)


router = APIRouter(prefix="/applications", tags=["applications"])


@router.post("", response_model=ApplicationRead)
async def create(data: ApplicationCreate):
    app = await create_application(data)
    return app


@router.get("", response_model=List[ApplicationRead])
async def list_all():
    return await list_applications()


@router.get("/{app_id}", response_model=ApplicationRead)
async def get(app_id: int):
    try:
        return await get_application(app_id)
    except Exception:
        raise HTTPException(status_code=404, detail="Application not found")


@router.patch("/{app_id}", response_model=ApplicationRead)
async def update(app_id: int, data: ApplicationUpdate):
    try:
        return await update_application(app_id, data)
    except Exception:
        raise HTTPException(status_code=404, detail="Application not found")

