import logging
import requests
import os
import time
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')
PROXY_URL = os.getenv('PROXY_URL')
API_URL = os.getenv('API_URL')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def get_order(title: str):
    req = requests.get(f'{API_URL}api/order/{title}')
    return req.json()


@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm ChūmonBot!\n To get order of a specific anime enter /order <ANIME-TITLE>")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    TEXT = "Welcome maester \n\n * To get order of a specific enter /order <ANIME-TITLE> and don't forget only to use lowercase and underscores instead of spaces \n\n * To request order enter /request ANIME_TITLE \n\n If u r having issues contact me @Itachiinthesky"
    rkm = InlineKeyboardMarkup(row_wigth=1)
    rkm.add(InlineKeyboardButton("Github", "https://github.com/Besufikad17/Chumon"))
    await message.answer(TEXT,reply_markup=rkm)

@dp.message_handler(commands=['request'])
async def submit_request(message: types.Message):
    anime_title = message.text[9:] 
    req = requests.post(f'{API_URL}/api/request/{anime_title}')
    if req.status_code == 200 or req.status_code == 400:
        await message.reply(req.json()['msg'])
    else:
        print(req.json())

@dp.message_handler(commands=['order'])
async def send_watch_order(message: types.Message):
    anime_title = message.text[7:]

    if anime_title is None:
        await message.reply("That's not quite right!! \n To get order of a specific anime enter /order <ANIME TITLE>")
    else:
        res = await get_order(anime_title)
        
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