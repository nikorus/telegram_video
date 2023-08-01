# import os
# from aiogram import Bot, types
# from aiogram.dispatcher import Dispatcher
# from aiogram.utils import executor
# from aiogram.types import InputTextMessageContent, InlineQueryResultArticle
# from dotenv import load_dotenv
#
# load_dotenv()  # This reads the environment variables inside .env
# token = os.getenv('TOKEN_INLINE')
# # инициализируем бот
# bot = Bot(token)
# # инициализируем диспетчер, передавая в него экземпляр бота
# # dp = Dispatcher(bot)
# #  добавляем параметр бота, где будет хранится информация
# dp = Dispatcher(bot=bot)
#
# executor.start_polling(dp, skip_updates=True)

import requests
from bs4 import BeautifulSoup
import re
import lxml


def searcher():
    response = requests.get('https://www.youtube.com/results?search_query=python')
    soup = BeautifulSoup(response.content, 'html.parser')

    search = soup.find_all('script')

    search = soup.find_all('script')[32]  # это номер в списке для примера
    key = '"videoID":"'
    # "videoId": "XKHEtdqhLK8"
    data = re.findall(key + r"([^*]{11})", str(search))  # [^*], обозначает любые символы кроме *!
    # data = re.findall(key, str(search))  # [^*], обозначает любые символы кроме *!
    print(data)
    # print(search)


searcher()
