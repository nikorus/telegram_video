'''
!!!  Когда мы писали весь код в одном файле - екораторы были обязательны и нужны
На текущем этапе Пролекта, когда создана многофайловая структура обработки сообщений пользователей
декораторы функций НЕ НУЖНЫ. Для наглядности их оставим закоментированными
'''
from keyboards.client_kb import kb_client

'''
В этот файл заносятся все, что находилось в файле мейн в разделе
Клиентская часть.
Здесь используются экземпляры объектов, которые создаются в мейн : dp  bot
Мы должны их сначала оттуда получить, а потом туда же вернуть
Решать это кодом можно, но грамоздко. Поэтому проще создать в папке проета вспомогательный файл create_bot.py
Его будем использовать ля проведения взаимоимпортов
В него перенесем из мейн - весь код ответственный за создание экземпляра бота
'''
'''
!!!! По тихому автор заменил названия функций  обработчиков команд в МЕЙН - а то
они были одним именем 
'''
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
    await bot.send_message(message.from_user.id,'Каждый день  9-00 до 20-00')

# @dp.message_handler(commands=['Расположение'])
async def pizza_place_command(message: types.Message):
    """ Декоратор обработки команды  Расположение """
    await bot.send_message(message.from_user.id, 'Дерибасовская - угол с Мясоедовской')
    # ниже строка для демонстрации как убрать пользовательскую клавиатуру . В файле client_kb нужно убрать
    # параметр , one_time_keyboard=True
    # await bot.send_message(message.from_user.id, 'Дерибасовская - угол с Мясоедовской', reply_markup=ReplyKeyboardRemove())


# @dp.message_handler(commands=['Меню'])
# async def pizza_menu_command(message : types.Message):
#     for ret in cur.execute('SELECT *FROM menu').fetchall():
#         await bot.send_photo(message.from_user.id, ret[0],f'{ret[1]}\nЦена {ret[-1]}')

'''
Регистрация хэндлеров нашего бота
Прописываем функцию (имя ее будет любое), которая запишет команды для регистрации Хэндлеров нашего бота, и эта же функция передаст
все хэндлеры в МЕЙН. В ней будет столько команд- сколько  у нас функций обработки сообщений 
на сейчас это 3
'''
#  dp : Dispatcher класс - это аннотация типа
#  .register_message_handler()  - это метод класса Диспетчер, который регистрирует хэндлеры для нашего бота
# внутри его параметров указываем
def register_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands= ['start', 'help'])
    dp.register_message_handler(pizza_open_command, commands=["Режим_работы"])
    dp.register_message_handler(pizza_place_command, commands=['Расположение'])



