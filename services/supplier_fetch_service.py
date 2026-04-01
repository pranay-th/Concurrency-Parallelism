import asyncio
import aiohttp
import requests
from utils.config import BASE_URL, ENDPOINTS
from utils.file_utils import save_json

async def fetch_one_async(session, name, endpoint):
    url = BASE_URL+endpoint
    async with session.get(url) as response:
        data = await response.json()
        save_json(f"{name}.json",data)
    return f"{name}.json"

async def fetch_all_concurrently():
    async with aiohttp.ClientSession() as session:
        tasks=[]

        for name,endpoint in ENDPOINTS.items():
            tasks.append(fetch_one_async(session,name,endpoint))

        await asyncio.gather(*tasks)

def fetch_all_sequentially():
    for name,endpoint in ENDPOINTS.items():
        url=BASE_URL+endpoint
        response=requests.get(url)
        response.raise_for_status()
        data=response.json()
        save_json(f"{name}.json",data)