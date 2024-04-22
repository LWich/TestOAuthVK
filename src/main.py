import os

from pydantic import BaseModel

import aiohttp
from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from dotenv import load_dotenv


load_dotenv()


CLIENT_SECRET = os.environ['OAUTH_VK_CLIENT_SECRET']


app = FastAPI()

app.mount("/static", StaticFiles(directory="src/static"), name="static")


templates = Jinja2Templates(directory="src/templates")


class DownloadRequest(BaseModel):
    url: str


async def get_profile_info(access_token: str) -> dict:
    url = 'https://api.vk.com/method/account.getProfileInfo?' \
          f'access_token={access_token}&v=5.199'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
        

async def get_user_friends(access_token: str) -> dict:
    url = 'https://api.vk.com/method/friends.get?' \
          f'access_token={access_token}&v=5.199'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()
        

@app.get('/auth/callback')
async def callback(code: str):
    url = f'https://oauth.vk.com/access_token?client_id=51858818&client_secret={CLIENT_SECRET}&code={code}&redirect_uri=https://prison-day.ru/callback&v=5.131&scope=65538'
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            json = await response.json()
            access_token = json['access_token']
            id = json['user_id']
            res =  RedirectResponse('https://prison-day.ru/auth/success')
            res.set_cookie('access_token', access_token)
            res.set_cookie('user_id', id)
            return res 


@app.get('/auth/success')
async def get_page(request: Request):
    return templates.TemplateResponse(
        request=request, name="success.html"
    )


@app.post('/auth/download')
async def download(req: DownloadRequest):
    async with aiohttp.ClientSession() as session:
        async with session.get(req.url) as response:
            return await response.json()
        