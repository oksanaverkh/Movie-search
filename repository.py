from sqlalchemy import select
from database import MovieOrm, new_session
from pydantic_models import MovieAdd, Movie


class MovieRepository:
    @classmethod
    async def add_movie(cls, movie: MovieAdd):
        async with new_session() as session:
            data = movie.model_dump()
            new_film = MovieOrm(**data)
            session.add(new_film)
            await session.flush()
            await session.commit()
            with open('movies_list.txt', 'a', encoding='utf-8') as file:
                file.write(f'\n{new_film.name}; {new_film.genre}; {
                           new_film.description}\n')
            return new_film.id

    @classmethod
    async def get_movies(cls):
        async with new_session() as session:
            query = select(MovieOrm)
            result = await session.execute(query)
            movie_models = result.scalars().all()
            movies = [Movie.model_validate(movie_model)
                      for movie_model in movie_models]
            return movies

    @classmethod
    async def fill_movies_table(cls):
        async with new_session() as session:
            with open('movies_list.txt', 'r', encoding='utf-8') as file:
                for row in file:
                    line = row.split(';')
                    data = {'name': line[0],
                            'genre': line[1][1:], 'description': line[2].replace('\n', '')}
                    movie = MovieOrm(**data)
                    session.add(movie)
            await session.flush()
            await session.commit()

    @classmethod
    async def find_movies_by_genre(cls, genre: str):
        async with new_session() as session:
            query = select(MovieOrm)
            result = await session.execute(query)
            movie_models = result.scalars().all()
            movies = [Movie.model_validate(movie_model)
                      for movie_model in movie_models if genre in movie_model.genre]
            return movies if movies else 'Таких фильмов нет'
