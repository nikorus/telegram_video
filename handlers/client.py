from keyboards.client_kb import kb_client

'''
!!!  Когда мы писали весь код в одном файле - екораторы были обязательны и нужны
На текущем этапе Пролекта, когда создана многофайловая структура обработки сообщений пользователей
декораторы функций НЕ НУЖНЫ. Для наглядности их оставим закоментированными
'''
# Для кода в Пайчарм  не обращать на серые импорты - они в нем не нужны

from aiogram import types, Dispatcher

'''
dp bot - импортируем из модуля create_bot
'''
from create_bot import dp, bot

'''импортируем клавиатуру
'''
from keyboards import client_kb

'''
Этот импорт , чтобы продемонстрировать как можно убрать пользовательскую клавиатуру
после выполнения к-л команды пользователя
'''
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db


# @dp.message_handler(commands=['start', 'help'])
async def command_start(message: types.Message):
    """ Декоратор обработки команд 'start', 'help'  """
    try:
        await bot.send_message(message.from_user.id, 'Приятного аппетита', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом через ЛС, напишите ему первый раз:https://t.me/Nikorus55_bot')


# @dp.message_handler(commands=["Режим_работы"])
async def pizza_open_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Каждый день  9-00 до 20-00')


'''Декоратор обработки команды  Расположение '''


# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    await bot.send_message(message.from_user.id, 'Дерибасовская - угол с Мясоедовской')
    # ниже строка для демонстрации как убрать пользовательскую клавиатуру . В файле client_kb нужно убрать
    # параметр , one_time_keyboard=True
    # await bot.send_message(message.from_user.id, 'Дерибасовская - угол с Мясоедовской',
    # reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message: types.Message):
    await sqlite_db.sql_read(message)


'''
Регистрация хэндлеров нашего бота
Прописываем функцию (имя ее будет любое), которая запишет команды для регистрации Хэндлеров нашего бота, 
и эта же функция передаст все хэндлеры в МЕЙН. В ней будет столько команд- сколько  у нас функций обработки сообщений 
на сейчас это 3
'''


#  dp : Dispatcher класс - это аннотация типа
#  .register_message_handler()  - это метод класса Диспетчер, который регистрирует хэндлеры для нашего бота
# внутри его параметров указываем
def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=["Режим_работы"])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])
