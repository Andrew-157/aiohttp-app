import aiohttp
import asyncio


async def get_users(session):

    async with session.get('http://localhost:8080/users', ssl=False) as response:

        print(f"Status code: {response.status}")
        response_json = await response.json()
        print(response_json)


async def get_user(session):

    user_id = 1

    async with session.get(f'http://localhost:8080/users/{user_id}', ssl=False) as response:

        print(f"Status code: {response.status}")
        response_json = await response.json()
        print(response_json)


async def create_user(session):

    user = {'user_id': 3, 'nickname': 'Mary', 'age': 19}

    async with session.post('http://localhost:8080/users', ssl=False, json=user) as response:

        print(f"Status code: {response.status}")
        response_json = await response.json()
        print(response_json)


async def update_user(session):

    user_id = 3
    user = {'user_id': user_id, 'nickname': 'Mary', 'age': 20}

    async with session.put(f'http://localhost:8080/users/{user_id}', ssl=False, json=user) as response:

        print(f"Status code: {response.status}")
        response_json = await response.json()
        print(response_json)


async def delete_user(session):

    user_id = 1

    async with session.put(f'http://localhost:8080/users/{user_id}', ssl=False) as response:

        print(f"Status code: {response.status}")


async def main():

    async with aiohttp.ClientSession()as session:
        await asyncio.gather(create_user(session),
                             update_user(session),
                             delete_user(session),
                             get_user(session),
                             get_users(session))


asyncio.run(main())
