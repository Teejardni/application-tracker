from fastapi import FastAPI
from contextlib import asynccontextmanager



@asynccontextmanager
def lifespan(app: FastAPI):
    yield

app = FastAPI()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    from datetime import datetime

    return {"status": "healthy", "timestamp": datetime.now().isoformat()}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)
