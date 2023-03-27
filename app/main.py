from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm.session import Session
from . import crud, schemas, database

app = FastAPI()


def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/users/", response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    return crud.create_user(db=db, user=user)


@app.get("/users/{user_id}/tasks", response_model=list[schemas.TaskOut])
def read_user_tasks(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.get_user_tasks(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user.tasks


@app.post("/users/{user_id}/tasks", response_model=schemas.TaskOut)
def create_task_for_user(user_id: int, task: schemas.TaskCreate, db: Session = Depends(get_db)):
    return crud.create_task_for_user(db=db, task=task, user_id=user_id)


@app.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, completed: bool, db: Session = Depends(get_db)):
    db_task = crud.update_task(db, task_id=task_id, completed=completed)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return db_task


@app.delete("/tasks/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db)):
    db_task = crud.delete_task(db, task_id=task_id)
    if db_task is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return {"detail": "Task deleted"}


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
