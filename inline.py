import os
from typing import List

from aiogram.utils import executor

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from dotenv import load_dotenv
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters import Text

load_dotenv()  # This reads the environment variables inside .env
token = os.getenv('TOKEN')
# инициализируем бот
bot = Bot(token)
# инициализируем диспетчер передавая в него экземпляр бота
# dp = Dispatcher(bot)
#  добавляем параметр бота, где будет хранится информация
dp = Dispatcher(bot=bot)

# это словарь для записи результатов голосования
# Однако - если бот будет перезапущен, то данные слваря будут утеряны
answ = dict()
'''
ИНЛАЙН - клавиатура и кнопки - это то, что появляется
Инициализируем класс ИНЛАЙН-клавиатуры и создаем объект, row_width=1 - значит по одной кнопки в ряду
создаем 2 кнопки и выводим их в бот одну под другой
text='Ссылка' - надпись на кнопке, url='https: - ссылка перехода 
'''

# 1 Создание Кнопки-ссылки

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
# inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Нажми меня', callback_data='www'))


'''1 хэндлер может обрабатывать несколько инлайн кнопок 
   Приведем пример кода, когда в чате происходит голосование и нужно подсчитать кол-во лайков и дислайков
   В этом случае объект inkb -  инлайе клавиатура должен быть определен иначе - поэтому закоментируем первый 
   и напишем другой. В клавиатуре определяется 2 кнопки с разными обработчиками
   Ниже в хэндлере -  выводится сообщение в чат и передается эта клавиатура с 2 кнопками
         '''
inkb = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text='Like', callback_data='like_1'),
                                             InlineKeyboardButton(text='DisLike', callback_data='like_-1'))


@dp.message_handler(commands='test')
async def test_commands(message: types.Message):
    await message.answer('Голосование за качество урока', reply_markup=inkb)


'''
    ниже надо добавить специальный обработчик события нажатия на эту кнопку
У нас теперь отлавливается не одно событие 'www', а 2. Чтобы их различить в одном обработчике - используем
встроенны в aiogram ФИЛЬТР - dispatcher.filters import Text
Text(startswith='like_'  применить фильтр типа Text, начать применение при совпадении с последовательностью 'like_' - 
у нас события отличны только после нижнего подчеркивания:  1 или -1
'''

@dp.callback_query_handler(Text(startswith='like_'))
#     параметр   - любое имя,   а главное его тип - CallbackQuery
async def www_call(callback: types.CallbackQuery):
    """
    здесь разбираем код для голосования;  callback - введенная нами переменная; data -  указываем тип данных
    split('_') -  Метод split() разделяет строку на список подстрок по разделителю - результатом буде 2 подстроки
    нас интересует вторая - в которой или 1 или -1 , поэтому указываем ее индекс в списке - [1]
    и приводим результат в целочисленное значение - int()
    """
    res = int(callback.data.split('_')[1])
    #  Заносить результаты будем в словарь  dict()
    #  проводим проверку для избежания повторного голосования - callback.from_user.id -это уникальный id  пользователя
    #   f'- это ф строка - она позволяет привести данные к типу, который можно использовать в операции if
    #   в res  будет 1 или -1
    if f'{callback.from_user.id}' not in answ:
        answ[f'{callback.from_user.id}'] = res
        #  бот ждет действий - или подтверждения что код хэндлера исполнен
        await callback.answer('Вы проголосовали')  # в этом случае выведется обычное сообщение с этим текстом
    else:
        #  бот ждет действий - или подтверждения что код хэндлера исполнен
        await callback.answer('Вы уже проголосовали', show_alert=True)


executor.start_polling(dp, skip_updates=True)
