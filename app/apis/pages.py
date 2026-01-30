from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from app.services.applications import list_applications
from app.core.templates import templates
from datetime import datetime, timezone

from app.services.applications import get_application
from app.services.events import list_events, add_event
from app.models.event import EventCreate
from app.models.enums import EventType


router = APIRouter(tags=["pages"])


@router.get("/", response_class=HTMLResponse)
async def kanban(request: Request):
    apps = await list_applications()

    columns = {
        "draft": [],
        "applied": [],
        "interview": [],
        "offer": [],
        "rejected": [],
        "withdrawn": [],
    }

    for app in apps:
        columns[app.status].append(app)

    return templates.TemplateResponse(
        "kanban.html",
        {
            "request": request,
            "columns": columns,
        },
    )


@router.get("/applications/{app_id}", response_class=HTMLResponse)
async def application_detail(request: Request, app_id: int):
    try:
        app = await get_application(app_id)
    except Exception:
        raise HTTPException(status_code=404)

    events = await list_events(app_id)

    return templates.TemplateResponse(
        "timeline.html",
        {
            "request": request,
            "application": app,
            "events": events,
            "event_types": [e.value for e in EventType],
        },)


@router.post("/applications/{app_id}/events")
async def create_event_from_form(request: Request, app_id: int):
    form = await request.form()

    event_type = form.get("event_type")
    metadata = form.get("metadata") or None

    await add_event(
        app_id,
        EventCreate(
            event_type=EventType(event_type),
            event_date=datetime.now(timezone.utc),
            metadata={"note": metadata} if metadata else None,
        ),
    )

    return RedirectResponse(
        url=f"/applications/{app_id}",
        status_code=303,
    )
