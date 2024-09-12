from sqlalchemy import select
from database import MovieOrm, new_session
from pydantic_models import MovieAdd, Movie

'''
Создание класса для работы с базой данных
'''


class MovieRepository:
    '''
    Метод для добавления фильма в базу данных.
    Принимает фильм, возвращает id добавленного фильма.
    '''
    @classmethod
    async def add_movie(cls, movie: MovieAdd):
        async with new_session() as session:
            # преобразование данных в модель Movie
            data = movie.model_dump()
            # создание нового фильма внутри приложения
            new_film = MovieOrm(**data)
            # добавление нового фильма в объект сессии
            session.add(new_film)
            # отправка запроса в базу данных, присвоение id
            await session.flush()
            # сохранение изменений в базе данных
            await session.commit()
            # запись добавленного фильма в файл со списком фильмов
            with open('movies_list.txt', 'a', encoding='utf-8') as file:
                file.write(f'\n{new_film.name}; {new_film.genre}; \ 
                           {new_film.description}\n')
            return new_film.id
    '''
    Метод для получения фильмов из базы данных.
    Возвращает список всех фильмов из базы.
    '''
    @classmethod
    async def get_movies(cls):
        async with new_session() as session:
            # запрос SELECT * к базе данных (выбор всех позиций)
            query = select(MovieOrm)
            # создание итератора, из которого нужно будет выбрать необходмые значения
            result = await session.execute(query)
            # выбор всех значений
            movie_models = result.scalars().all()
            # создание списка фильмов
            movies = [Movie.model_validate(movie_model)
                      for movie_model in movie_models]
            return movies
    
    '''
    Метод для заполнения базы данных фильмами из файла.
    Запускается при старте приложения.
    '''
    @classmethod
    async def fill_movies_table(cls):
        async with new_session() as session:
            # открытие файла на чтение
            with open('movies_list.txt', 'r', encoding='utf-8') as file:
                for row in file:
                    line = row.split(';')
                    # построчная обработка данных, приведение к формату словаря
                    data = {'name': line[0],
                            'genre': line[1][1:], 'description': line[2].replace('\n', '')}
                    # создание экземпляра фильма для добавления в базу
                    movie = MovieOrm(**data)
                    # добавление фильма в базу данных
                    session.add(movie)
            # отправка запроса в базу данных, присвоение id
            await session.flush()
            # сохранение изменений в базе данных
            await session.commit()
    '''
    Метод для поиска фильма по заданному жанру.
    Принимает строку (жанр), возвращает список фильмов указанного жанра, либо ответ, что фильмы отсутствуют.
    '''
    @classmethod
    async def find_movies_by_genre(cls, genre: str):
        async with new_session() as session:
            # запрос SELECT * к базе данных (выбор всех позиций)
            query = select(MovieOrm)
            # создание итератора, из которого нужно будет выбрать необходмые значения
            result = await session.execute(query)
            # выбор всех значений
            movie_models = result.scalars().all()
            # создание списка фильмов с условием соответствия фильма выбранному жанру
            movies = [Movie.model_validate(movie_model)
                      for movie_model in movie_models if genre in movie_model.genre]
            return movies if movies else 'Таких фильмов нет'
