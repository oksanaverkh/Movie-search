from pydantic import BaseModel, ConfigDict

'''
Основной класс для добавления нового фильма.
Наследуется от BaseModel, который предоставляет функциональность валидации данных.
'''


class MovieAdd(BaseModel):
    name: str
    description: str | None = None
    genre: str


'''
Класс Movie расширяет MovieAdd, добавляя поле id. 
Включает параметр model_config, который позволяет конфигурировать поведение модели при загрузке/сохранении.
'''


class Movie(MovieAdd):
    id: int
    model_config = ConfigDict(from_attributes=True)


'''
Класс MovieId является расширением BaseModel и содержит только одно поле id, которое служит уникальным идентификатором фильма.
'''


class MovieId(BaseModel):
    id: int
