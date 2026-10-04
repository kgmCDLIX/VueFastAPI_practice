from pydantic import BaseModel, ConfigDict


class PipePartCreate(BaseModel):
    name: str
    pipe_id: int
    condition: str | None = None
    length: str | None = None


class PipePartUpdate(BaseModel):
    name: str | None = None
    pipe_id: int | None = None
    condition: str | None = None
    length: str | None = None


class PipePartRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    pipe_id: int
    condition: str | None = None
    length: str | None = None