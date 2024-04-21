import os
import json 

import aiohttp
from fastapi import (FastAPI, APIRouter, Request,
                     Response)

from dotenv import load_dotenv


load_dotenv()


CLIENT_SECRET = os.environ['OAUTH_VK_CLIENT_SECRET']


auth = APIRouter(prefix='/auth')

app = FastAPI()
app.include_router(auth)


async def get_profile_info(access_token: str) -> dict:
    url = 'https://api.vk.com/method/account.getProfileInfo?' \
          f'access_token={access_token}&v=5.199'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()


@auth.get('/callback')
async def callback(code: str):
    url = f'https://oauth.vk.com/access_token?client_id=51858818&client_secret={CLIENT_SECRET}&code={code}&redirect_uri=https://prison-day.ru/callback&v=5.131&scope=65538'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            print(json)
            access_token = json['access_token']
            profile = await get_profile_info(access_token)
            print(profile)
