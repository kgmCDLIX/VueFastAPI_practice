from pydantic import BaseModel


class PipePartCreate(BaseModel):
    name: str
    pipe_id: int
    condition: str | None = None
    length: str | None = None


class PipePartRead(BaseModel):
    id: int
    name: str
    pipe_id: int
    condition: str | None = None
    length: str | None = None