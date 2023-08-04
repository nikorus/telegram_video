import hashlib
import os
import hashlib
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
from dotenv import load_dotenv

load_dotenv()  # This reads the environment variables inside .env
token = os.getenv('TOKEN_INLINE')
# инициализируем бот
bot = Bot(token)
# инициализируем диспетчер, передавая в него экземпляр бота
# dp = Dispatcher(bot)
#  добавляем параметр бота, где будет хранится информация
dp = Dispatcher(bot=bot)

'''
Ниже вариант использования  BeautifulSoup для парсинга ютьюба
Он оказался сложным к разбору

import requests
from bs4 import BeautifulSoup
import re


def searcher():
    response = requests.get('https://www.youtube.com/results?search_query=python')
    soup = BeautifulSoup(response.content, 'html.parser')

    search = soup.find_all('script')  # это номер в списке для примера
    # search = soup.find_all('script')[32]  # это номер в списке для примера
    # key = '"videoID":"'
    # data = re.findall(key+r"([^*]{11})", str(search)) #  [^*], обозначает любые символы кроме *!
    # print(data)
    print(search)


searcher()

'''

from youtube_search import YoutubeSearch


def searcher(text):
    res = YoutubeSearch(text, max_results=10).to_dict()
    return res


@dp.inline_handler()
async def inline_handler(query: types.InlineQuery):
    text = query.query or "echo"
    links = searcher(text)

    articles = [types.InlineQueryResultArticle(
        id=hashlib.md5(f'{link["id"]}'.encode()).hexdigest(),
        title=f'{link["title"]}',
        url=f'https://www.youtube.com/watch&v={link["id"]}',
        thumb_url=f'{link["thumbnails"][0]}',
        input_message_content=types.InputTextMessageContent(
            message_text=f'https://www.youtube.com/watch&v={link["id"]}')
    ) for link in links]
    await query.answer(articles, cache_time=1, is_personal=True)


executor.start_polling(dp, skip_updates=True)
