from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.session import AsyncSessionLocal
from app.repositories.task_repo import TaskRepository
from app.services.task_service import TaskService


async def get_session():
    async with AsyncSessionLocal() as session:
        yield session


def get_task_service(
    session: AsyncSession = Depends(get_session),
) -> TaskService:
    repo = TaskRepository(session)
    return TaskService(repo)
