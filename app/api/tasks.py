from typing import Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status

from app.schemas.task import Task, TaskCreate, TaskUpdate
from app.services.deps import get_task_service
from app.services.task_service import TaskService

router = APIRouter(prefix="/tasks", tags=["Tasks"])


@router.post(
    "",
    response_model=Task,
    status_code=status.HTTP_201_CREATED,
    summary="Создать задачу",
)
async def create_task(
    payload: TaskCreate,
    service: TaskService = Depends(get_task_service),
):
    return await service.create_task(payload)


@router.get(
    "/{task_id}",
    response_model=Task,
    summary="Получить задачу по ID",
)
async def get_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
):
    task = await service.get_task(task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.get(
    "",
    response_model=list[Task],
    summary="Получить список задач",
)
async def list_tasks(
    status: Optional[str] = Query(None, description="Фильтр по статусу"),
    priority: Optional[int] = Query(None, ge=1, le=5),
    include_deleted: bool = Query(False),
    limit: int = Query(20, ge=1, le=100),
    offset: int = Query(0, ge=0),
    service: TaskService = Depends(get_task_service),
):
    return await service.list_tasks(
        status=status,
        priority=priority,
        include_deleted=include_deleted,
        limit=limit,
        offset=offset,
    )


@router.put(
    "/{task_id}",
    response_model=Task,
    summary="Обновить задачу",
)
async def update_task(
    task_id: UUID,
    payload: TaskUpdate,
    service: TaskService = Depends(get_task_service),
):
    task = await service.update_task(task_id, payload)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@router.delete(
    "/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить задачу (soft delete)",
)
async def delete_task(
    task_id: UUID,
    service: TaskService = Depends(get_task_service),
):
    ok = await service.delete_task(task_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Task not found")
