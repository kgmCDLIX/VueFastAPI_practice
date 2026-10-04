from pydantic import BaseModel, ConfigDict


class PipeCreate(BaseModel):
    name: str
    vertex_start_id: int
    vertex_end_id: int
    condition: str | None = None
    diameter: str | None = None
    material: str | None = None


class PipeUpdate(BaseModel):
    name: str | None = None
    vertex_start_id: int | None = None
    vertex_end_id: int | None = None
    condition: str | None = None
    diameter: str | None = None
    material: str | None = None


class PipeRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    vertex_start_id: int
    vertex_end_id: int
    condition: str | None = None
    diameter: str | None = None
    material: str | None = None