import requests
import datetime
import asyncio
import aiohttp
from models import Swapi, init_models, Session, engine
from more_itertools import chunked

MAX_CHUNK = 10

async def get_people(pers_id, session):
    async with session.get(f'https://swapi.py4e.com/api/people/{pers_id}/') as response:
        json_data = await response.json()
        return json_data

# async def main_03():
#     s = aiohttp.ClientSession()
#     coroutine_01 = get_people(1, s)
#     response_01 = await coroutine_01
#
#     print(", ".join(response_01['vehicles']))


async def insert_people(list_people_json):
    async with Session() as session:
        orm_objects = [Swapi(birth_year=person_json['birth_year'], eye_color=person_json['eye_color'], films_list=", ".join(person_json['films']), gender=person_json['gender'], hair_color=person_json['hair_color'], height=person_json['height'], homeworld=person_json['homeworld'], mass=person_json['mass'], name=person_json['name'], skin_color=person_json['skin_color'], species_list=", ".join(person_json['species']), starships_list=", ".join(person_json['starships']), vehicles_list=", ".join(person_json['vehicles'])) for person_json in list_people_json]
        session.add_all(orm_objects)
        await session.commit()


async def main():
    await init_models()
    async with aiohttp.ClientSession() as session:
        p_ids = chunked(range(1, 101), MAX_CHUNK)
        for p_ids_ch in p_ids:
            coroutines = [get_people(p_id, session) for p_id in p_ids_ch]
            results = await asyncio.gather(*coroutines)
            asyncio.create_task(insert_people(results))
            print(results)
        main_task = asyncio.current_task()
        all_tasks = asyncio.all_tasks()
        all_tasks.remove(main_task)
        await asyncio.gather(*all_tasks)


# async def main():
#     # await init_orm()
#     async with aiohttp.ClientSession() as session:
#         p_ids = chunked(range(1, 101), MAX_CHUNK)
#         for p_ids_ch in p_ids:
#             coroutines = [get_people(p_id, session) for p_id in p_ids_ch]
#             results = await asyncio.gather(*coroutines)
#             await insert_people(results)
#             print(results)





asyncio.run(main())
