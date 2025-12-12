from fastapi import FastAPI

from app.api.tasks import router as tasks_router
from app.api.health import router as health_router
from app.db.base import Base
from app.db.session import engine

app = FastAPI(
    title="Task Management API",
    description=(
        "Асинхронный REST API для управления задачами.\n\n"
        "Архитектура: API → Service → Repository → PostgreSQL"
    ),
    version="1.0.0",
)

# Подключаем роутеры
app.include_router(tasks_router)
app.include_router(health_router)


@app.on_event("startup")
async def on_startup() -> None:
    """
    Инициализация приложения.

    В рамках тестового задания схема БД создаётся автоматически.
    В production-окружении здесь обычно используются миграции (Alembic).
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("shutdown")
async def on_shutdown() -> None:
    """
    Корректное завершение работы приложения.
    """
    await engine.dispose()
