"""
В этот файл заносятся все, что находилось в файле мейн в разделе
Общая часть
"""
from aiogram import types, Dispatcher
import json
import string

'''
dp - импортируем из модуля create_bot
Для PyCharm - это не нужно. Оставил как артефакт
'''
from create_bot import dp

"""Добавляем фильтр отсечки мата
Создаем базу данных мата. Для этого испjльзуем джейсон файл
"""


# @dp.message_handler()
# декорируемая ф-я не нужна, так как мы Регистрируем хэндлер в register_handlers_other(dp: Dispatcher):
async def echo_send(message: types.Message):  # имя функции любое
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')} \
            .intersection(set(json.load(open('cenz.json', "r")))) != set():
        await message.reply('Нецензурные выражения запрещены')
        await message.delete()


def register_handlers_other(dp: Dispatcher):
    dp.register_message_handler(echo_send)
