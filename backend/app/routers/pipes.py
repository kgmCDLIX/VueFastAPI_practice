from fastapi import APIRouter

from ..schemas.pipe import PipeCreate, PipeRead


router = APIRouter(
    prefix="/pipes",
    tags=["pipes"]
)


pipes = [
    {
        "id": 1,
        "name": "Труба 1",
        "vertex_start_id": 1,
        "vertex_end_id": 2,
        "condition": "Исправна",
        "diameter": "530 мм",
        "material": "Сталь",
    }
]


@router.get("/", response_model=list[PipeRead])
def get_pipes():
    return pipes


@router.post("/", response_model=PipeRead)
def create_pipe(pipe: PipeCreate):
    new_pipe = {
        "id": len(pipes) + 1,
        "name": pipe.name,
        "vertex_start_id": pipe.vertex_start_id,
        "vertex_end_id": pipe.vertex_end_id,
        "condition": pipe.condition,
        "diameter": pipe.diameter,
        "material": pipe.material,
    }

    pipes.append(new_pipe)

    return new_pipe