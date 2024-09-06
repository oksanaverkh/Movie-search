from pydantic import BaseModel, ConfigDict


class MovieAdd(BaseModel):
    name: str
    description: str | None = None
    genre: str


class Movie(MovieAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


class MovieId(BaseModel):
    id: int
