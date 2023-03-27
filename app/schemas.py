from pydantic import BaseModel


class UserCreate(BaseModel):
    username: str


class TaskCreate(BaseModel):
    title: str
    description: str


class UserCreate(BaseModel):
    username: str


class UserOut(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True


class TaskCreate(BaseModel):
    title: str
    description: str


class TaskOut(BaseModel):
    id: int
    title: str
    description: str
    completed: bool
    owner_id: int

    class Config:
        orm_mode = True


class TaskUpdate(BaseModel):
    completed: bool
