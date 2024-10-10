import os
import asyncpg
import asyncio
# import sys
#
# if sys.platform:
#     asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
#
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'LLllMMmmqwerty654321')
POSTGRES_USER = os.getenv('POSTGRES_USER', 'postgres')
POSTGRES_DB = os.getenv('POSTGRES_DB', 'swapi')
POSTGRES_HOST = os.getenv('POSTGRES_HOST', '127.0.0.1')
# POSTGRES_HOST = os.getenv('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = os.getenv('POSTGRES_PORT', '5437')

#
PG_DSN = f'postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}'
#
engine = create_async_engine(PG_DSN)

Session = async_sessionmaker(engine, expire_on_commit=False)



class Base(DeclarativeBase, AsyncAttrs):
    pass
#
class Swapi(Base):
    __tablename__ = 'swapi_people'

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    birth_year: Mapped[str] = mapped_column(String(30))
    eye_color: Mapped[str] = mapped_column(String(30))
    films_list: Mapped[str] = mapped_column(String(500))
    gender: Mapped[str] = mapped_column(String(30))
    hair_color: Mapped[str] = mapped_column(String(30))
    height: Mapped[str] = mapped_column(String(30))
    homeworld: Mapped[str] = mapped_column(String(30))
    mass: Mapped[str] = mapped_column(String(30))
    name: Mapped[str] = mapped_column(String(30))
    skin_color: Mapped[str] = mapped_column(String(30))
    species_list: Mapped[str] = mapped_column(String(500))
    starships_list: Mapped[str] = mapped_column(String(500))
    vehicles_list: Mapped[str] = mapped_column(String(500))


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)





