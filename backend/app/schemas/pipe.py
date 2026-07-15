from pydantic import BaseModel


class PipeCreate(BaseModel):
    name: str
    vertex_start_id: int
    vertex_end_id: int
    condition: str | None = None
    diameter: str | None = None
    material: str | None = None


class PipeRead(BaseModel):
    id: int
    name: str
    vertex_start_id: int
    vertex_end_id: int
    condition: str | None = None
    diameter: str | None = None
    material: str | None = None