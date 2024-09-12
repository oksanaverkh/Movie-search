from fastapi import FastAPI
from repository import MovieRepository
from router import router
from database import create_table, delete_table
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    # создание базы данных при запуске приложения
    await create_table()
    print("Base created")
    # заполнение базы данных фильмами из файла
    await MovieRepository.fill_movies_table()
    print("Table filled")
    yield
    # удаление базы данных при прекращении работы приложения
    await delete_table()
    print("Base deleted")

'''
Создание приложения, подключение роутера
'''
app = FastAPI(lifespan=lifespan)
app.include_router(router)
