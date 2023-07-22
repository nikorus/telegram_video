import os

'''
В модулях пакета хэндлерз  используются экземпляры объектов, которые создаются в мейн : dp  bot
Мы должны их сначала оттуда получить, а потом туда же вернуть
Решать это кодом можно, но грамоздко. Поэтому проще создать в папке проекта вспомогательный файл create_bot.py
Его будем использовать ля проведения взаимоимпортов. В него перенесем из мейн - весь код ответственный за создание экземпляра бота
'''
""" импортируем ос"""

'''выбираем в качестве хранилища для хранения цепочек вопрос-ответ диалога
пользователя с ботом - класс для хранения данных в оперативной памяти
'''
from aiogram.contrib.fsm_storage.memory import MemoryStorage

# создаем экземпляр класса
storage = MemoryStorage()
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher

from dotenv import load_dotenv

load_dotenv()  # This reads the environment variables inside .env

token = os.getenv('TOKEN')
# инициализируем бот
bot = Bot(token)
# инициализируем диспетчер передавая в него экземпляр бота
# dp = Dispatcher(bot)
#  добавляем параметр бота, где будет хранится информация
dp = Dispatcher(bot, storage=storage)
