from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


'''
Cоздание асинхронного подключения, которое будет отвечать за отправку запросов в базу данных engine 
с использованием драйвера для асинхронного кода aiosqlitе. 
Дополнительно создается фабрика сессий new_session.
'''
engine = create_async_engine("sqlite+aiosqlite:///movies.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)

'''
Создание родительского класса для модели данных - таблицы в базе данных SQLAlchemy
'''


class Model(DeclarativeBase):
    pass


'''
Создание модели данных - таблицы в базе данных SQLAlchemy
'''


class MovieOrm(Model):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    genre: Mapped[str]
    description: Mapped[str | None]


'''
Создание таблиц в базе данных
'''


async def create_table():
    async with engine.begin() as connector:
        await connector.run_sync(Model.metadata.create_all)

'''
Удаление таблиц в базе данных
'''


async def delete_table():
    async with engine.begin() as connector:
        await connector.run_sync(Model.metadata.drop_all)
