from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pipe import Pipe
from app.models.vertex import Vertex
from app.schemas.pipe import PipeCreate, PipeRead, PipeUpdate


router = APIRouter(
    prefix="/pipes",
    tags=["pipes"],
)


@router.get("/", response_model=list[PipeRead])
def get_pipes(db: Session = Depends(get_db)):
    return db.scalars(select(Pipe)).all()


@router.get("/{pipe_id}", response_model=PipeRead)
def get_pipe(
    pipe_id: int,
    db: Session = Depends(get_db),
):
    pipe = db.get(Pipe, pipe_id)

    if pipe is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe not found",
        )

    return pipe


@router.post("/", response_model=PipeRead, status_code=201)
def create_pipe(
    pipe: PipeCreate,
    db: Session = Depends(get_db),
):
    if pipe.vertex_start_id == pipe.vertex_end_id:
        raise HTTPException(
            status_code=400,
            detail="Start and end vertices must be different",
        )

    start_vertex = db.get(Vertex, pipe.vertex_start_id)
    end_vertex = db.get(Vertex, pipe.vertex_end_id)

    if start_vertex is None:
        raise HTTPException(
            status_code=404,
            detail="Start vertex not found",
        )

    if end_vertex is None:
        raise HTTPException(
            status_code=404,
            detail="End vertex not found",
        )

    new_pipe = Pipe(**pipe.model_dump())

    db.add(new_pipe)
    db.commit()
    db.refresh(new_pipe)

    return new_pipe


@router.patch("/{pipe_id}", response_model=PipeRead)
def update_pipe(
    pipe_id: int,
    pipe_data: PipeUpdate,
    db: Session = Depends(get_db),
):
    pipe = db.get(Pipe, pipe_id)

    if pipe is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe not found",
        )

    update_data = pipe_data.model_dump(exclude_unset=True)

    start_id = update_data.get(
        "vertex_start_id",
        pipe.vertex_start_id,
    )

    end_id = update_data.get(
        "vertex_end_id",
        pipe.vertex_end_id,
    )

    if start_id == end_id:
        raise HTTPException(
            status_code=400,
            detail="Start and end vertices must be different",
        )

    if db.get(Vertex, start_id) is None:
        raise HTTPException(
            status_code=404,
            detail="Start vertex not found",
        )

    if db.get(Vertex, end_id) is None:
        raise HTTPException(
            status_code=404,
            detail="End vertex not found",
        )

    for field, value in update_data.items():
        setattr(pipe, field, value)

    db.commit()
    db.refresh(pipe)

    return pipe


@router.delete("/{pipe_id}", status_code=204)
def delete_pipe(
    pipe_id: int,
    db: Session = Depends(get_db),
):
    pipe = db.get(Pipe, pipe_id)

    if pipe is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe not found",
        )

    db.delete(pipe)
    db.commit()