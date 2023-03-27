import httpx
import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app import crud, main, models, schemas, database

# Set up a test database and session
TEST_DATABASE_URL = "sqlite:///./test_todo.db"
test_engine = create_engine(TEST_DATABASE_URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
database.Base.metadata.create_all(bind=test_engine)


# Dependency override for tests
def get_test_db():
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the get_db function in the app
main.app.dependency_overrides[main.get_db] = get_test_db

client = TestClient(main.app)


def test_create_user():
    response = client.post("/users/", json={"username": "test_user"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "username": "test_user"}


def test_create_task_for_user():
    response = client.post("/users/1/tasks", json={"title": "Test Task", "description": "Test Description"})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "title": "Test Task", "description": "Test Description", "completed": False,
                               "owner_id": 1}


def test_read_user_tasks():
    response = client.get("/users/1/tasks")
    assert response.status_code == status.HTTP_200_OK
    tasks = response.json()
    assert len(tasks) == 1
    assert tasks[0] == {"id": 1, "title": "Test Task", "description": "Test Description", "completed": False,
                        "owner_id": 1}


def test_update_task():
    response = client.put("/tasks/1", json={"completed": True})
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"id": 1, "title": "Test Task", "description": "Test Description", "completed": True,
                               "owner_id": 1}


def test_delete_task():
    response = client.delete("/tasks/1")
    assert response.status_code == status.HTTP_200_OK
    assert response.json() == {"detail": "Task deleted"}


def test_read_non_existent_user_tasks():
    response = client.get("/users/999/tasks")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_create_task_for_non_existent_user():
    response = client.post("/users/999/tasks", json={"title": "Test Task 2", "description": "Test Description 2"})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "User not found"}


def test_update_non_existent_task():
    response = client.put("/tasks/999", json={"completed": True})
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


def test_delete_non_existent_task():
    response = client.delete("/tasks/999")
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert response.json() == {"detail": "Task not found"}


def teardown_module():
    database.Base.metadata.drop_all(bind=test_engine)
