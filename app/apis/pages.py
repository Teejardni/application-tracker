from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse

from app.services.applications import list_applications
from app.core.templates import templates

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

