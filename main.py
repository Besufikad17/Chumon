import logging
import aiohttp
import requests
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types

load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')
PROXY_URL = os.getenv('PROXY_URL')
PROXY_AUTH = aiohttp.BasicAuth(login='login', password=os.getenv('PROXY_PWD'))

logging.basicConfig(level=logging.INFO)

# bot = Bot(token=API_TOKEN, proxy=PROXY_URL, proxy_auth=PROXY_AUTH)
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_order(title: str):
    req = requests.get(f'http://localhost:4000/api/order/{title}')
    print(req.json())
    return req.json()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm ChūmonBot!\n To get order of a specific anime enter /order <ANIME TITLE>")


@dp.message_handler(commands=['order'])
async def send_watch_order(message: types.Message):
    anime_title = message.text.split(' ')[1]
    if anime_title is None:
        await message.reply("That's not quite right!! \n To get order of a specific anime enter /order <ANIME TITLE>")
    else:
        get_order(anime_title)
        await message.reply(get_order(anime_title)[0]['order'], parse_mode = "Markdown")


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)