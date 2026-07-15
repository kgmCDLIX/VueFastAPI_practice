from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import auth, pipe_parts, pipes, vertices
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {"message": "Backend is working"}


@app.get("/api/hello")
def hello():
    return {"message": "Привет из FastAPI"}

app.include_router(auth.router)
app.include_router(pipes.router)
app.include_router(vertices.router)
app.include_router(pipe_parts.router)
