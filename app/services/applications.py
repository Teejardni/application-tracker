from datetime import datetime

from app.schemas.application import Application
from app.schemas.event import ApplicationEvent
from app.models.application import ApplicationCreate, ApplicationUpdate
from app.models.enums import ApplicationStatus, EventType


async def create_application(data: ApplicationCreate) -> Application:
    app = await Application.create(
        company=data.company,
        role_title=data.role_title,
        location=data.location,
        source=data.source,
        date_applied=data.date_applied,
        status=ApplicationStatus.applied.value,
        salary_min=data.salary_min,
        salary_max=data.salary_max,
        relocation=data.relocation,
        visa_sponsorship=data.visa_sponsorship,
        notes=data.notes,
    )

    # invariant: every application starts with an "applied" event
    await ApplicationEvent.create(
        application=app,
        event_type=EventType.applied.value,
        event_date=datetime.utcnow(),
        metadata=None,
    )

    return app


async def update_application(
    app_id: int,
    data: ApplicationUpdate,
) -> Application:
    app = await Application.get(id=app_id)

    update_fields = data.model_dump(exclude_unset=True)

    if "status" in update_fields:
        update_fields["status"] = update_fields["status"].value

    for field, value in update_fields.items():
        setattr(app, field, value)

    await app.save()
    return app


async def get_application(app_id: int) -> Application:
    return await Application.get(id=app_id)


async def list_applications():
    return await Application.all().order_by("-last_updated")

