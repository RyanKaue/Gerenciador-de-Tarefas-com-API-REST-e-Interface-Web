from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime

from app.database import get_db
from app.schemas.task import TaskCreate, TaskResponse, TaskUpdate
from app.crud.task import get_tasks, get_task, create_task, update_task, delete_task
from app.utils.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/tasks", tags=["tarefas"])

@router.post("/", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task_endpoint(
    task: TaskCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Cria uma nova tarefa para o usuário autenticado."""
    return create_task(db=db, task=task, user_id=current_user.id)

@router.get("/", response_model=List[TaskResponse])
def read_tasks(
    skip: int = 0,
    limit: int = 100,
    status: Optional[str] = None,
    priority: Optional[str] = None,
    due_date_before: Optional[datetime] = None,
    order_by: str = "created_at",
    order_direction: str = "desc",
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retorna todas as tarefas do usuário com filtros opcionais."""
    tasks = get_tasks(
        db=db, 
        user_id=current_user.id, 
        skip=skip, 
        limit=limit,
        status=status,
        priority=priority,
        due_date_before=due_date_before,
        order_by=order_by,
        order_direction=order_direction
    )
    return tasks

@router.get("/{task_id}", response_model=TaskResponse)
def read_task(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Retorna uma tarefa específica do usuário."""
    task = get_task(db=db, task_id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    return task

@router.put("/{task_id}", response_model=TaskResponse)
def update_task_endpoint(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Atualiza uma tarefa específica do usuário."""
    task = update_task(db=db, task_id=task_id, user_id=current_user.id, task_update=task_update)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    return task

@router.delete("/{task_id}", response_model=TaskResponse)
def delete_task_endpoint(
    task_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Exclui uma tarefa específica do usuário."""
    task = delete_task(db=db, task_id=task_id, user_id=current_user.id)
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Tarefa não encontrada"
        )
    return task
