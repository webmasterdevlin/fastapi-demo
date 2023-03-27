from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.orm.session import Session
from app import schemas, crud
from app.database import get_db
from app.schemas import TaskUpdate

router = APIRouter(
    prefix="/api",
)


@router.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@router.get("/users/{user_id}/tasks", response_model=list[schemas.TaskOut])
def read_user_tasks(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_tasks(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.tasks


@router.post("/users/{user_id}/tasks", response_model=schemas.TaskOut)
def create_task_for_user(user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return crud.create_task_for_user(db, task=task, user_id=user_id)


@router.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task_update: TaskUpdate, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id=task_id, completed=task_update.completed)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}
