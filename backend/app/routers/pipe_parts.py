from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pipe import Pipe
from app.models.pipe_part import PipePart
from app.schemas.pipe_part import (
    PipePartCreate,
    PipePartRead,
    PipePartUpdate,
)


router = APIRouter(
    prefix="/pipe-parts",
    tags=["pipe-parts"],
)


@router.get("/", response_model=list[PipePartRead])
def get_pipe_parts(db: Session = Depends(get_db)):
    return db.scalars(select(PipePart)).all()


@router.get("/{part_id}", response_model=PipePartRead)
def get_pipe_part(
    part_id: int,
    db: Session = Depends(get_db),
):
    part = db.get(PipePart, part_id)

    if part is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe part not found",
        )

    return part


@router.post("/", response_model=PipePartRead, status_code=201)
def create_pipe_part(
    part: PipePartCreate,
    db: Session = Depends(get_db),
):
    pipe = db.get(Pipe, part.pipe_id)

    if pipe is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe not found",
        )

    new_part = PipePart(**part.model_dump())

    db.add(new_part)
    db.commit()
    db.refresh(new_part)

    return new_part


@router.patch("/{part_id}", response_model=PipePartRead)
def update_pipe_part(
    part_id: int,
    part_data: PipePartUpdate,
    db: Session = Depends(get_db),
):
    part = db.get(PipePart, part_id)

    if part is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe part not found",
        )

    update_data = part_data.model_dump(exclude_unset=True)

    if "pipe_id" in update_data:
        pipe = db.get(Pipe, update_data["pipe_id"])

        if pipe is None:
            raise HTTPException(
                status_code=404,
                detail="Pipe not found",
            )

    for field, value in update_data.items():
        setattr(part, field, value)

    db.commit()
    db.refresh(part)

    return part


@router.delete("/{part_id}", status_code=204)
def delete_pipe_part(
    part_id: int,
    db: Session = Depends(get_db),
):
    part = db.get(PipePart, part_id)

    if part is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe part not found",
        )

    db.delete(part)
    db.commit()