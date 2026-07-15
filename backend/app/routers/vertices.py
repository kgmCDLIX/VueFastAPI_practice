from fastapi import APIRouter

from ..schemas.vertex import VertexCreate, VertexRead

router = APIRouter(
    prefix="/vertices",
    tags=["vertices"]
)


vertices = [
    {
        "id": 1,
        "name": "Скважина 101",
        "type": "Скважина",
        "condition": "Работает",
    },
    {
        "id": 2,
        "name": "Скважина 102",
        "type": "Скважина",
        "condition": "Работает",
    },
]


@router.get("/", response_model=list[VertexRead])
def get_vertices():
    return vertices


@router.post("/", response_model=VertexRead)
def create_vertex(vertex: VertexCreate):
    new_vertex = {
        "id": len(vertices) + 1,
        "name": vertex.name,
        "type": vertex.type,
        "condition": vertex.condition,
    }

    vertices.append(new_vertex)

    return new_vertex