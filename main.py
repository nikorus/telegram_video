""" импортируем ос"""
import os

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
@dp.message_handler()
# декорируемая ф-я
async def echo_send(message: types.Message):  # имя функции любое
    """
    Декоратор обработки сообщения пользователя Hello
    :param message:
    :return:
    """
    if message.text == 'Hello':
        await message.answer('Hi, my darling !')

    # await message.answer(message.text)  # 1-й способ
    # await message.reply(message.text)  # 2-й способ тоже, о с повторением исходного сообщения
    # await bot.send_message(message.from_user.id, message.text)
    # #3-й способ - только если пользователь уже обращался к боту


# здесь получается айди пользователя и посылается ему сообщение


# запуск бота с параметром пропускать обновления - все сообщения которые приходят боту в офлайн
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
