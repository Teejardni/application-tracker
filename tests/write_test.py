import asyncio
from datetime import date, datetime

from app.core.db import init_db, close_db
from app.services.applications import create_application
from app.services.events import add_event
from app.models.application import ApplicationCreate
from app.models.event import EventCreate
from app.models.enums import EventType


async def main():
    await init_db()

    # Create application
    app = await create_application(
        ApplicationCreate(
            company="Acme Corp",
            role_title="Backend Engineer",
            location="Remote",
            source="LinkedIn",
            date_applied=date.today(),
        )
    )

    print("Created application:", app.id, app.status)

    # Add interview event
    event = await add_event(
        app.id,
        EventCreate(
            event_type=EventType.interview_scheduled,
            event_date=datetime.utcnow(),
            metadata={"round": 1},
        ),
    )

    print("Added event:", event.event_type)

    # Fetch again to verify status
    await app.refresh_from_db()
    print("Updated status:", app.status)

    await close_db()


if __name__ == "__main__":
    asyncio.run(main())

