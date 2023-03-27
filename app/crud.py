from sqlalchemy.orm import Session
from .models import User, Task
from .schemas import UserCreate, TaskCreate


def create_user(db: Session, user: UserCreate):
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def create_task_for_user(db: Session, task: TaskCreate, user_id: int):
    db_task = Task(title=task.title, description=task.description, owner_id=user_id)
    db.add(db_task)
    db.commit()
    db.refresh(db_task)
    return db_task


def get_user_tasks(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def update_task(db: Session, task_id: int, completed: bool):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db_task.completed = completed
        db.commit()
        db.refresh(db_task)
        return db_task


def delete_task(db: Session, task_id: int):
    db_task = db.query(Task).filter(Task.id == task_id).first()
    if db_task:
        db.delete(db_task)
        db.commit()
        return db_task
