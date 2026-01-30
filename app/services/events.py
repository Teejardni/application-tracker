from app.schemas.application import Application
from app.schemas.event import ApplicationEvent
from app.models.event import EventCreate
from app.models.enums import EventType, ApplicationStatus


EVENT_TO_STATUS = {
    EventType.applied: ApplicationStatus.applied,
    EventType.interview_scheduled: ApplicationStatus.interview,
    EventType.interview_completed: ApplicationStatus.interview,
    EventType.offer_received: ApplicationStatus.offer,
    EventType.offer_accepted: ApplicationStatus.offer,
    EventType.rejection: ApplicationStatus.rejected,
    EventType.withdrawn: ApplicationStatus.withdrawn,
}


async def add_event(
    application_id: int,
    data: EventCreate,
) -> ApplicationEvent:
    app = await Application.get(id=application_id)

    event = await ApplicationEvent.create(
        application=app,
        event_type=data.event_type.value,
        event_date=data.event_date,
        metadata=data.metadata,
    )

    # update application status if this event implies one
    new_status = EVENT_TO_STATUS.get(data.event_type)
    if new_status is not None:
        app.status = new_status.value
        await app.save()

    return event


async def list_events(application_id: int):
    return (
        await ApplicationEvent.filter(application_id=application_id)
        .order_by("event_date")
    )

