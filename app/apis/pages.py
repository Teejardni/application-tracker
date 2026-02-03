from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse

from app.services.applications import list_applications, create_application
from app.core.templates import templates
from datetime import date, datetime, timezone

from app.services.applications import get_application
from app.services.events import list_events, add_event
from app.services.scrape import scrape_job_posting
from app.models.event import EventCreate
from app.models.enums import EventType
from app.models.application import ApplicationCreate


router = APIRouter(prefix="/ui", tags=["pages"])


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


@router.get("/applications/new", response_class=HTMLResponse)
async def new_application(request: Request, url: str | None = None):
    prefill = {}
    error = None

    if url:
        try:
            prefill = scrape_job_posting(url)
        except Exception as exc:
            error = f"Unable to fetch details from that link: {exc}"

    return templates.TemplateResponse(
        "new_application.html",
        {
            "request": request,
            "prefill": prefill,
            "error": error,
            "today": date.today().isoformat(),
        },
    )


@router.post("/applications", response_class=RedirectResponse)
async def create_application_from_form(request: Request):
    form = await request.form()

    date_applied_raw = form.get("date_applied")
    date_applied = (
        date.fromisoformat(date_applied_raw)
        if date_applied_raw
        else date.today()
    )

    salary_min_raw = form.get("salary_min")
    salary_max_raw = form.get("salary_max")
    relocation_raw = form.get("relocation")

    await create_application(
        ApplicationCreate(
            company=form.get("company"),
            role_title=form.get("role_title"),
            location=form.get("location") or None,
            source=form.get("source") or None,
            date_applied=date_applied,
            salary_min=int(salary_min_raw) if salary_min_raw else None,
            salary_max=int(salary_max_raw) if salary_max_raw else None,
            relocation=True if relocation_raw else None,
            visa_sponsorship=form.get("visa_sponsorship") or None,
            notes=form.get("notes") or None,
        )
    )

    return RedirectResponse(url="/ui/", status_code=303)


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
