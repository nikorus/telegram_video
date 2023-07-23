import os
from typing import List

from aiogram.utils import executor

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

load_dotenv()  # This reads the environment variables inside .env
token = os.getenv('TOKEN')
# инициализируем бот
bot = Bot(token)
# инициализируем диспетчер передавая в него экземпляр бота
# dp = Dispatcher(bot)
#  добавляем параметр бота, где будет хранится информация
dp = Dispatcher(bot=bot)

'''
ИНЛАЙН - клавиатура и кнопки - это то, что появляется
Инициализируем класс ИНЛАЙН-клавиатуры и создаем объект, row_width=1 - значит по одной кнопки в ряду
создаем 2 кнопки и выводим их в бот одну под другой
text='Ссылка' - надпись на кнопке, url='https: - ссылка перехода 
'''

# 1 Создание Кнопки-сслки

urlkb = InlineKeyboardMarkup(row_width=1)
urlButton = InlineKeyboardButton(text='Ссылка', url='https://youtube.com')
urlButton2 = InlineKeyboardButton(text='Ссылка 2', url='https://google.com')

# создадим список с кнопками, который будем использовать для добавления списком -
x: list[InlineKeyboardButton] = [InlineKeyboardButton(text='Ссылка3', url='https://youtube.com'),
                                 InlineKeyboardButton(text='Ссылка 4', url='https://google.com'),
                                 InlineKeyboardButton(text='Ссылка5', url='https://youtube.com')]
# *x - это распаковка списка
# ограничение row_width=1 - не распространяется на row(*x) - они будут в одном ряду
# insert(Inl -  не добавляет кнопки в текущий ряд - кт нет места и он ставит ряд ниже
urlkb.add(urlButton, urlButton2).row(*x).insert(InlineKeyboardButton(text='Ссылка6', url='https://youtube.com'))


# Хэндлер вызова вышесозданной инлайн клавиатуры
@dp.message_handler(commands='ссылки')
async def url_command(message: types.Message):
    await message.answer('Ссылочки:', reply_markup=urlkb)


# 2 Создание Inline-Кнопки  c callback

'''
Создаем экземпляр объекта инлайн клавиатуры с коллбэком  и сразу добаляем ей кнопку
callback_data='www' - этот параметр указывает на некоторое событие , это мб и даже просто ввод символов www
это событие отправляется БОТу , коорый будет его отлавливать - Для этого нужно написать  спец. хэндлер 
- @dp.message_handler(commands='test'). 
Передавать можно (вместо www) и некоторые данные которые будут использоваться нашим кодом 
message.answer('Инлайн кнопка', reply_markup=inkb) - На команду test  пользователя - бот напишет ИНЛАЙН кнопка и 
передаст клавиатуру - в которой будет кнопка с надписью Нажми меня
'''
inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Нажми меня', callback_data='www'))


@dp.message_handler(commands='test')
async def test_commands(message: types.Message):
    await message.answer('Инлайн кнопка', reply_markup=inkb)


#     ниже надо добавить специальный обработчик события нажатия на эту кнопку
# Для того чтобы отлолвить событие 'www'
@dp.callback_query_handler(text='www')
#     параметр   - любое имя,   а главное его тип - CallbackQuery
async def www_call(callback: types.CallbackQuery):
    #      здесь можно записать любой код и тп , но мы для примера - просто ответим пользователю;
    #      callback - введенная нами переменная
    # await callback.answer('Вы нажали инлайн кнопку')  # в этом случае выведется всплывающее сообщение с этим текстом
    await callback.message.answer('Вы нажали инлайн кнопку')  # в этом случае выведется обычное сообщение с этим текстом
    # но в обоих случаях - бот ждет действий - или подтвержденияБ что код хэндлера исполнен. Подтвердим это просто так:
    # await callback.answer()
#      или написать ТЕКСТ - который высветится в виде всплывающего сообщения
#     await callback.answer('Нажата инлайн Кнопка')
#      а в этом случае будет сообщение - в виде Уведомления - алерта , которое нужно подтвердить нажав ОК
    await callback.answer('Нажата инлайн Кнопка', show_alert=True)

    '''1 хэндлер может обрабатывать несколько инлайн кнопок 
    Приведем пример кода, когда в чате происходит голосование и нужно подсчитать кол-во лайков и дислайков
          '''


executor.start_polling(dp, skip_updates=True)
