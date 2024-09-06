from datetime import datetime
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

engine = create_async_engine("sqlite+aiosqlite:///movies.db")
new_session = async_sessionmaker(engine, expire_on_commit=False)


class Model(DeclarativeBase):
    pass


class MovieOrm(Model):
    __tablename__ = 'movies'
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str]
    genre: Mapped[str]
    description: Mapped[str | None]


async def create_table():
    async with engine.begin() as connector:
        await connector.run_sync(Model.metadata.create_all)


async def delete_table():
    async with engine.begin() as connector:
        await connector.run_sync(Model.metadata.drop_all)
