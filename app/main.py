from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.core.db import init_db, close_db
from app.core.settings import settings
from app.apis.applications import router as applications_router
from app.apis.events import router as events_router
from fastapi.staticfiles import StaticFiles
from app.apis.pages import router as pages_router



@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(title="Job Application Tracker by IG", debug=settings.debug, lifespan=lifespan)


app.include_router(applications_router)
app.include_router(events_router)
app.include_router(pages_router)
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from datetime import datetime

    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
