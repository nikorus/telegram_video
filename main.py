""" импортируем ос"""
import os

import json
import string

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from dotenv import load_dotenv

load_dotenv()  # This reads the environment variables inside .env

token = os.getenv('TOKEN')
# инициализируем бот
bot = Bot(token)
# инициализируем диспетчер передавая в него экземпляр бота
dp = Dispatcher(bot)

async def on_startup(_):
    """ Функция начального сообщения в консоль о начале работы бота  """
    print('Бот вышел в онлайн')

# *************************КЛИЕНСКАЯ ЧАСТЬ **********************
@dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    """ Декоратор обработки команд 'start', 'help'  """
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита')
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему первый раз:https://t.me/Nikorus55_bot')

@dp.message_handler(commands=["Режим_работы"])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id,'Каждый день  9-00 до 20-00')

@dp.message_handler(commands=['Расположение'])
async def command_start(message: types.Message):
    """ Декоратор обработки команды  Расположение """
    await bot.send_message(message.from_user.id, 'Дерибасовская - угол с Мясоедовской')


# @dp.message_handler(commands=['Меню'])
# async def pizza_menu_command(message : types.Message):
#     for ret in cur.execute('SELECT *FROM menu').fetchall():
#         await bot.send_photo(message.from_user.id, ret[0],f'{ret[1]}\nЦена {ret[-1]}')

# *************************АДМИНСКАЯ ЧАСТЬ **********************

# *************************ОБЩАЯ ЧАСТЬ **********************


# Прописываем декоратор , который будет обработываьть сообщения пришедшие в месседжер
"""Добавляем фильтр отсечки мата
Создаем базу данных мата. Для этого исплльзуем джейсон файл
"""

# Это просто приер того, как читать джкйсон-файл в пайтон
with open('cenz.json', 'r') as f:
    data = f.read()
    json_data = json.loads(data)
@dp.message_handler()
# декорируемая ф-я
async def echo_send(message: types.Message):  # имя функции любое
    """
    Декоратор обработки сообщения пользователя:  сначала проверяем через генератор множеств
     - множество нужно сформировать:  перебираем сообщение пользователя разбитое (for i in message.text.split(' '))
    по разделитею - пробелу.Получаем список слов в сообщении. Потом переводим все в нижний регистр. Избавляемся от маскировочных символов мата:
    *,! и тд. -  для этого используем метод для списков - в него передается макетизменений для символов в строке:
     translate(str.maketrans('','',string.punctuation) - первые ковычки -перечень что менять, вторые- на  что менять
    вместо, третий параметр - какие символы ужно убрать - используем стандартный модуль  string.punctuation, который позволяет искать все символы, а не буквы
   Формируем новое множество .intersection(set(json.load(''))), которое мы получаем читая файл cenz.json Если полученное множество после проверки  не пустое
   - выведем сообщение пользователю 'Нецензурные выражения запрещены' и удаляем его сообщение. А если совпадений нет - множество пересечений будет пустым - то все ок

    :param message:
    :return:
    """

    if {i.lower().translate(str.maketrans('','',string.punctuation))for i in message.text.split(' ')}\
        .intersection(set(json.load(open('cenz.json', "r")))) != set():
        await message.reply('Нецензурные выражения запрещены')
        await message.delete()
'''
Делаем проверку на совпадение слов запрещенных и пришедших от пользователя. 
Именно поэтому используются множества - так как они делают это быстро. Для этого
используется метод пересечения множеств-intersection, которое является результатом проверки всего
выражения внутри if
'''

# запуск бота с параметром пропускать обновления - все сообщения которые приходят боту в офлайн
# третий параметр задает функцию которая выполняеся после начала работы программы
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
