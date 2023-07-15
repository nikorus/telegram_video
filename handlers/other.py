'''
В этот файл заносятся все, что находилось в файле мейн в разделе
Общая часть
'''
from aiogram import types, Dispatcher
import json

import string

'''
dp - импортируем из модуля create_bot
'''
from create_bot import dp


"""Добавляем фильтр отсечки мата
Создаем базу данных мата. Для этого исплльзуем джейсон файл
"""


# @dp.message_handler()
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

    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cenz.json', "r")))) != set():
        await message.reply('Нецензурные выражения запрещены')
        await message.delete()


'''
Делаем проверку на совпадение слов запрещенных и пришедших от пользователя. 
Именно поэтому используются множества - так как они делают это быстро. Для этого
используется метод пересечения множеств-intersection, которое является результатом проверки всего
выражения внутри if
'''
'''
Прописываем функцию (имя ее будет любое), которая запишет команды для регистрации Хэндлеров нашего бота, и эта же функция передаст
все хэндлеры в МЕЙН. В ней будет столько коман- сколько  у нас функций обработки сообщений 
на сейчас это 1
, commands= ['start', 'help'] - убираем так как команд у этой функции нет
'''


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
