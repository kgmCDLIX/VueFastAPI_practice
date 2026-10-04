from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from .database import Base, engine
from .routers import auth, pipe_parts, pipes, vertices
from . import models


Base.metadata.create_all(bind=engine)

app = FastAPI()


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "Backend is working",
    }


@app.get("/db-check")
def db_check():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1"))

        return {
            "database": "connected",
            "result": result.scalar_one(),
        }


app.include_router(auth.router)
app.include_router(pipes.router)
app.include_router(vertices.router)
app.include_router(pipe_parts.router)