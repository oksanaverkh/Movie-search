from fastapi import APIRouter, Depends
from repository import MovieRepository
from pydantic_models import MovieAdd

'''
Создание роутера
'''
router = APIRouter(prefix='/movies', tags=['фильмы'])

'''
Эндпойнт для добавления фильма
'''


@router.post('')
async def add_movie(movie: MovieAdd = Depends()):
    new_movie_id = await MovieRepository.add_movie(movie)
    return {"id": new_movie_id}

'''
Эндпойнт для получения всех фильмов
'''


@router.get('_all')
async def get_movies():
    movies = await MovieRepository.get_movies()
    return movies

'''
Эндпойнт для получения фильмов по заданному жанру
'''


@router.get('_by_genre')
async def find_movies_by_genre(genre: str):
    movies = await MovieRepository.find_movies_by_genre(genre)
    return movies
