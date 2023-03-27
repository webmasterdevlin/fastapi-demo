from fastapi import FastAPI
from app import routers

app = FastAPI(title="Todo App Demo", version="0.1.0")

app.include_router(routers.router)

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8000)
