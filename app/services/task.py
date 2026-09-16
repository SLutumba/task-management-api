from sqlalchemy.orm import Session
from app.exceptions import InvalidDateTimeError, TaskNotFoundError
from app.models import Task
from app.schemas.task import CreateTaskRequest
from datetime import datetime

def create_task(
        db: Session,
        request: CreateTaskRequest,
        user_id: int
    ) -> Task:

    if (request.due_date is not None 
        and (request.due_date < datetime.now())):
        raise InvalidDateTimeError(
            f"Invalid due date entered. The date cannot be before today's date: {datetime.today().date()}"
        )
    print(request.status)
    new_task = Task(
        user_id=user_id,
        title=request.title,
        description=request.description,
        status=request.status.value,
        priority=request.priority.value,
        due_date=request.due_date
    )

    db.add(new_task)

    try:
        db.commit()
    except Exception:
        db.rollback()
        raise
    db.refresh(new_task)

    return new_task

def get_tasks(
        db: Session,
        user_id: int
    ) -> list[Task]:

    # query the db for all tasks that have the specified user id. 
    tasks = (
        db.query(Task)
        .filter(Task.user_id == user_id)
        .all()
    )
    
    return tasks

def get_task(
        db: Session, 
        user_id: int, 
        task_id: int
    ) -> Task:

    task = (
        db.query(Task)
        .filter(Task.id == task_id, Task.user_id == user_id)
        .first()
    )

    if task is None:
        raise TaskNotFoundError(
            "Task doesn't exist"
        )

    return task