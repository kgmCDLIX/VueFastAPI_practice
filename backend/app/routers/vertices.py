from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.vertex import Vertex
from app.schemas.vertex import VertexCreate, VertexRead, VertexUpdate


router = APIRouter(
    prefix="/vertices",
    tags=["vertices"],
)


@router.get("/", response_model=list[VertexRead])
def get_vertices(db: Session = Depends(get_db)):
    return db.scalars(select(Vertex)).all()


@router.get("/{vertex_id}", response_model=VertexRead)
def get_vertex(
    vertex_id: int,
    db: Session = Depends(get_db),
):
    vertex = db.get(Vertex, vertex_id)

    if vertex is None:
        raise HTTPException(
            status_code=404,
            detail="Vertex not found",
        )

    return vertex


@router.post("/", response_model=VertexRead, status_code=201)
def create_vertex(
    vertex: VertexCreate,
    db: Session = Depends(get_db),
):
    new_vertex = Vertex(**vertex.model_dump())

    db.add(new_vertex)
    db.commit()
    db.refresh(new_vertex)

    return new_vertex


@router.patch("/{vertex_id}", response_model=VertexRead)
def update_vertex(
    vertex_id: int,
    vertex_data: VertexUpdate,
    db: Session = Depends(get_db),
):
    vertex = db.get(Vertex, vertex_id)

    if vertex is None:
        raise HTTPException(
            status_code=404,
            detail="Vertex not found",
        )

    update_data = vertex_data.model_dump(exclude_unset=True)

    for field, value in update_data.items():
        setattr(vertex, field, value)

    db.commit()
    db.refresh(vertex)

    return vertex


@router.delete("/{vertex_id}", status_code=204)
def delete_vertex(
    vertex_id: int,
    db: Session = Depends(get_db),
):
    vertex = db.get(Vertex, vertex_id)

    if vertex is None:
        raise HTTPException(
            status_code=404,
            detail="Vertex not found",
        )

    db.delete(vertex)
    db.commit()