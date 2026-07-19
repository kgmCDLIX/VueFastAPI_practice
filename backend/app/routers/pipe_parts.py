from fastapi import APIRouter

from app.schemas.pipe_part import PipePartCreate, PipePartRead


router = APIRouter(
    prefix="/pipe-parts",
    tags=["pipe parts"]
)


pipe_parts = [
    {
        "id": 1,
        "name": "Часть трубы 1.1",
        "pipe_id": 1,
        "condition": "Исправна",
        "length": "50 м",
    },
    {
        "id": 2,
        "name": "Часть трубы 1.2",
        "pipe_id": 1,
        "condition": "Требует осмотра",
        "length": "70 м",
    },
]


@router.get("/", response_model=list[PipePartRead])
def get_pipe_parts():
    return pipe_parts


@router.post("/", response_model=PipePartRead)
def create_pipe_part(pipe_part: PipePartCreate):
    new_pipe_part = {
        "id": len(pipe_parts) + 1,
        "name": pipe_part.name,
        "pipe_id": pipe_part.pipe_id,
        "condition": pipe_part.condition,
        "length": pipe_part.length,
    }

    pipe_parts.append(new_pipe_part)

    return new_pipe_part