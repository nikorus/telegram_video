from create_bot import dp
from aiogram.utils import executor
from handlers import client, admin, other
from data_base import sqlite_db
'''
!!!  Когда мы писали весь код в одном файле - декораторы были обязательны и нужны
На текущем этапе Проекта, когда создана многофайловая структура обработки сообщений пользователей
декораторы функций НЕ НУЖНЫ. Для наглядности их оставим закоментированными
'''
'''
dp - импортируем из модуля create_bot
'''

async def on_startup(_):
    """ Функция начального сообщения в консоль о начале работы бота  и подключение БД"""
    print('Бот вышел в онлайн')
    sqlite_db.sql_start()


'''
Импортируем сюда функции из модулей client.py  other.py  admin.py
функции register_handlers_
!!! Порядок импорта функций имеет значение
'''

client.register_handlers_client(dp)
admin.register_handlers_admin(dp)
other.register_handlers_other(dp)

# запуск бота с параметром пропускать обновления - все сообщения которые приходят боту в офлайн
# третий параметр задает функцию которая выполняеся после начала работы программы
executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
