import json
import aiohttp

async def req(url):
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response = (await response.text()).encode().decode()
            data = json.loads(response)
            return data


async def reqPost(url, data):
    async with aiohttp.ClientSession() as session:
        async with session.post(url, data=data) as response:
            response = (await response.text()).encode().decode()
            data = json.loads(response)
            return data
