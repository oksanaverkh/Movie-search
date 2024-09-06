from fastapi import FastAPI
from repository import MovieRepository
from router import router
from database import create_table, delete_table
from contextlib import asynccontextmanager


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_table()
    print("Base created")
    await MovieRepository.fill_movies_table()
    print("Table filled")
    yield
    await delete_table()
    print("Base deleted")


app = FastAPI(lifespan=lifespan)
app.include_router(router)
