from fastapi import FastAPI

from app.api.tasks import router
from app.db.base import Base
from app.db.session import engine
from app.api.health import router as health_router

app = FastAPI(
    title="Task Management API",
    version="1.0.0",
)

app.include_router(health_router)
app.include_router(router)


@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
