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
from youtube_search import YoutubeSearch


def searcher():
    res = YoutubeSearch('python hb studio telegram бот', max_results=1).to_dict()
    with open('../text2.py', 'w', encoding='utf-8') as r:
        r.write(str(res))


searcher()


