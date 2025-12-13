from datetime import datetime
from typing import Optional
from uuid import UUID
from app.schemas.enums import TaskStatus

from pydantic import BaseModel, Field


class TaskBase(BaseModel):
    title: str = Field(
        ...,
        min_length=1,
        max_length=200,
        description="Название задачи",
        examples=["Implement authentication"],
    )
    description: Optional[str] = Field(
        None,
        max_length=2000,
        description="Описание задачи",
        examples=["Add JWT-based authentication"],
    )
    status: TaskStatus = Field(
        TaskStatus.new,
        description="Статус задачи",
    )
    priority: int = Field(
        3,
        ge=1,
        le=5,
        description="Приоритет задачи (1 — высокий, 5 — низкий)",
    )


class TaskCreate(TaskBase):
    """
    Схема для создания задачи
    """
    pass


class TaskUpdate(BaseModel):
    """
    Схема для частичного обновления задачи
    """
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, max_length=2000)
    status: Optional[TaskStatus]
    priority: Optional[int] = Field(None, ge=1, le=5)


class Task(TaskBase):
    """
    Схема ответа API
    """
    id: UUID = Field(description="UUID задачи")
    created_at: datetime = Field(description="Дата создания (UTC)")
    updated_at: datetime = Field(description="Дата последнего обновления (UTC)")
    deleted_at: Optional[datetime] = Field(
        None,
        description="Дата удаления (soft delete)",
    )

    class Config:
        from_attributes = True
