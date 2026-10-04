from pydantic import BaseModel, ConfigDict


class VertexCreate(BaseModel):
    name: str
    type: str
    condition: str | None = None


class VertexUpdate(BaseModel):
    name: str | None = None
    type: str | None = None
    condition: str | None = None


class VertexRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    type: str
    condition: str | None = None