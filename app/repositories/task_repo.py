from datetime import datetime
from typing import List, Optional
from uuid import UUID

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate


class TaskRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, data: TaskCreate) -> Task:
        task = Task(**data.model_dump())
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get(self, task_id: UUID) -> Task | None:
        return await self.session.get(Task, task_id)

    async def update(self, task_id: UUID, data: TaskUpdate) -> Task | None:
        task = await self.get(task_id)
        if not task:
            return None

        for k, v in data.model_dump(exclude_unset=True).items():
            setattr(task, k, v)

        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def soft_delete(self, task_id: UUID) -> bool:
        task = await self.get(task_id)
        if not task or task.deleted_at:
            return False

        task.deleted_at = datetime.utcnow()
        await self.session.commit()
        return True

    async def list(
            self,
            *,
            status: Optional[str],
            priority: Optional[int],
            include_deleted: bool,
            limit: int,
            offset: int,
    ) -> list[Task]:
        stmt = select(Task)

        if not include_deleted:
            stmt = stmt.where(Task.deleted_at.is_(None))

        if status:
            stmt = stmt.where(Task.status == status)

        if priority:
            stmt = stmt.where(Task.priority == priority)

        stmt = stmt.limit(limit).offset(offset)

        result = await self.session.execute(stmt)
        return list(result.scalars().all())