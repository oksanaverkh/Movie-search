from fastapi import APIRouter, Depends
from repository import MovieRepository
from pydantic_models import MovieAdd

router = APIRouter(prefix='/movies', tags=['фильмы'])


@router.post('')
async def add_movie(movie: MovieAdd = Depends()):
    new_movie_id = await MovieRepository.add_movie(movie)
    return {"id": new_movie_id}


@router.get('_all')
async def get_movies():
    movies = await MovieRepository.get_movies()
    return movies


@router.get('_by_genre')
async def find_movies_by_genre(genre: str):
    movies = await MovieRepository.find_movies_by_genre(genre)
    return movies
