import logging
import requests
import os
from dotenv import load_dotenv
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()


API_TOKEN = os.getenv('API_TOKEN')
API_URL = os.getenv('API_URL')

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)


async def get_order(title: str):
    req = requests.get(f'{API_URL}api/order/{title}')
    return req.json()

def get_list():
    req = requests.get(f'{API_URL}api/list')
    list_of_anime = []
    for i in req.json():
        list_of_anime.append(i['title'])
    return list_of_anime

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Hi!\nI'm ChūmonBot!\n To get order of a specific anime enter /order <ANIME-TITLE>")

@dp.message_handler(commands=['help'])
async def send_help(message: types.Message):
    TEXT = "Welcome maester \n\n * To get order of a specific enter /order <ANIME-TITLE> and don't forget only to use lowercase \n\n * To request order enter /request ANIME_TITLE \n\n If u r having issues contact me @Itachiinthesky"
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


@dp.message_handler(commands=['list'])
async def send_list(message: types.Message):
    TEXT = ""
    lists = get_list()
    for list_ in lists:
        TEXT += f"\n {list_}"
    await message.answer(TEXT)

@dp.message_handler(commands=['order'])
async def send_watch_order(message: types.Message):
    anime_title = message.text[7:]
    anime_title = anime_title.lower()

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
    await message.answer("Read instructions using /help mf")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)