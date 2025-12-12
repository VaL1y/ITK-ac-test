from uuid import UUID

from app.repositories.task_repo import TaskRepository
from app.schemas.task import TaskCreate, TaskUpdate
from app.models.task import Task


class TaskService:
    def __init__(self, repo: TaskRepository):
        self.repo = repo

    async def create_task(self, data: TaskCreate) -> Task:
        return await self.repo.create(data)

    async def get_task(self, task_id: UUID) -> Task | None:
        return await self.repo.get(task_id)

    async def update_task(self, task_id: UUID, data: TaskUpdate) -> Task | None:
        return await self.repo.update(task_id, data)

    async def delete_task(self, task_id: UUID) -> bool:
        return await self.repo.soft_delete(task_id)

    async def list_tasks(
        self,
        *,
        status: str | None,
        priority: int | None,
        include_deleted: bool,
        limit: int,
        offset: int,
    ) -> list[Task]:
        return await self.repo.list(
            status=status,
            priority=priority,
            include_deleted=include_deleted,
            limit=limit,
            offset=offset,
        )
