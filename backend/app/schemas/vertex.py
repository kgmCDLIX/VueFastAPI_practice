from pydantic import BaseModel

class VertexCreate(BaseModel):
    name: str
    type: str
    condition: str | None = None

class VertexRead(BaseModel):
    id: int
    name: str
    type: str
    condition: str | None = None