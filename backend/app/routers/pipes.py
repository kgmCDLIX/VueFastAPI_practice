from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from geoalchemy2.shape import from_shape, to_shape
from shapely.geometry import LineString

from app.database import get_db
from app.models.pipe import Pipe
from app.models.pipe_part import PipePart
from app.models.vertex import Vertex
from app.schemas.pipe import PipeCreate, PipeRead, PipeUpdate


router = APIRouter(
    prefix="/pipes",
    tags=["pipes"],
)


def build_pipe_geometry(
    start_vertex: Vertex,
    end_vertex: Vertex,
):
    """
    Строит LINESTRING между двумя вершинами.
    """

    if start_vertex.geometry is None:
        raise HTTPException(
            status_code=400,
            detail="У начальной вершины не заданы координаты",
        )

    if end_vertex.geometry is None:
        raise HTTPException(
            status_code=400,
            detail="У конечной вершины не заданы координаты",
        )

    start_point = to_shape(
        start_vertex.geometry
    )

    end_point = to_shape(
        end_vertex.geometry
    )

    line = LineString(
        [
            start_point.coords[0],
            end_point.coords[0],
        ]
    )

    return from_shape(
        line,
        srid=4326,
    )


def get_vertices_for_pipe(
    db: Session,
    start_id: int,
    end_id: int,
):
    """
    Проверяет вершины трубы и возвращает их.
    """

    if start_id == end_id:
        raise HTTPException(
            status_code=400,
            detail="Начальная и конечная вершины должны отличаться",
        )

    start_vertex = db.get(
        Vertex,
        start_id,
    )

    if start_vertex is None:
        raise HTTPException(
            status_code=404,
            detail="Начальная вершина не найдена",
        )

    end_vertex = db.get(
        Vertex,
        end_id,
    )

    if end_vertex is None:
        raise HTTPException(
            status_code=404,
            detail="Конечная вершина не найдена",
        )

    return start_vertex, end_vertex


@router.get(
    "/",
    response_model=list[PipeRead],
)
def get_pipes(
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(Pipe)
    ).all()


@router.get(
    "/{pipe_id}",
    response_model=PipeRead,
)
def get_pipe(
    pipe_id: int,
    db: Session = Depends(get_db),
):
    pipe = db.get(
        Pipe,
        pipe_id,
    )

    if pipe is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe not found",
        )

    return pipe


@router.post(
    "/",
    response_model=PipeRead,
    status_code=201,
)
def create_pipe(
    pipe: PipeCreate,
    db: Session = Depends(get_db),
):
    start_vertex, end_vertex = (
        get_vertices_for_pipe(
            db,
            pipe.vertex_start_id,
            pipe.vertex_end_id,
        )
    )

    new_pipe = Pipe(
        **pipe.model_dump()
    )

    # Геометрия создаётся автоматически
    new_pipe.geometry = build_pipe_geometry(
        start_vertex,
        end_vertex,
    )

    db.add(new_pipe)

    db.commit()
    db.refresh(new_pipe)

    return new_pipe


@router.patch(
    "/{pipe_id}",
    response_model=PipeRead,
)
def update_pipe(
    pipe_id: int,
    pipe_data: PipeUpdate,
    db: Session = Depends(get_db),
):
    pipe = db.get(
        Pipe,
        pipe_id,
    )

    if pipe is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe not found",
        )

    update_data = (
        pipe_data.model_dump(
            exclude_unset=True
        )
    )

    start_id = update_data.get(
        "vertex_start_id",
        pipe.vertex_start_id,
    )

    end_id = update_data.get(
        "vertex_end_id",
        pipe.vertex_end_id,
    )

    start_vertex, end_vertex = (
        get_vertices_for_pipe(
            db,
            start_id,
            end_id,
        )
    )

    # Обновляем обычные поля
    for field, value in update_data.items():
        setattr(
            pipe,
            field,
            value,
        )

    # Пересчитываем геометрию трубы
    pipe.geometry = build_pipe_geometry(
        start_vertex,
        end_vertex,
    )

    # Сохраняем изменение трубы,
    # чтобы geometry гарантированно была готова
    db.flush()

    # Пока PipePart повторяет геометрию Pipe.
    # Позже, если понадобится,
    # сделаем отдельную геометрию участков.
    db.execute(
        update(PipePart)
        .where(
            PipePart.pipe_id == pipe.id
        )
        .values(
            geometry=pipe.geometry
        )
    )

    db.commit()
    db.refresh(pipe)

    return pipe


@router.delete(
    "/{pipe_id}",
    status_code=204,
)
def delete_pipe(
    pipe_id: int,
    db: Session = Depends(get_db),
):
    pipe = db.get(
        Pipe,
        pipe_id,
    )

    if pipe is None:
        raise HTTPException(
            status_code=404,
            detail="Pipe not found",
        )

    db.delete(pipe)
    db.commit()