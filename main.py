import logging
import aiohttp
import requests
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')
PROXY_URL = os.getenv('PROXY_URL')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


def get_order(title: str):
    req = requests.get(f'http://localhost:4000/api/order/{title}')
    return req.json()


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm ChūmonBot!\n To get order of a specific anime enter /order <ANIME-TITLE>")


@dp.message_handler(commands=['order'])
async def send_watch_order(message: types.Message):
    anime_title = message.text[7:]
    print(anime_title)
    if anime_title is None:
        await message.reply("That's not quite right!! \n To get order of a specific anime enter /order <ANIME TITLE>")
    else:
        res = get_order(anime_title)
        
        if res is None or len(res) == 0:
            await message.reply("Can't find the anime :( try alternative titles")
        else:
            rkm = InlineKeyboardMarkup(row_wigth=1)
            rkm.add(InlineKeyboardButton("More..", "https://www.reddit.com/r/anime/wiki/watch_order/"))
            await message.answer(res[0]['order'], parse_mode="MARKDOWN", reply_markup=rkm)


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(message.text)


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)