from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# В хэндлерах commands  - это обработка команд, те пользователь вводит / перед текстом

ID = None
'''Создаем класс состояний  с любым именем , который наследуется от базового класса StatesGroup 
'''


class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


'''Доступ к командам админа дб только у администратора. Для этого нужно сделать праверку на администратора
'''


# Получаем ID текущего модератора
# is_chat_admin=   - это фильтр
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    # предаем кнопки добавления меню Админу и добавим клавиатуру админу
    await bot.send_message(message.from_user.id, 'Что будем делать шеф ?', reply_markup=admin_kb.button_case_admin)
    await message.delete()


'''Ниже расположен Базовый хендлер, который запускает машину состояний
'''


# Начало диалога загрузки нового пункта Меню
# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

    # Ловим первый ответ и пишем его в словарь
    ''' После перехода машины в состояние фото : Здесь отлавливается первый ответ пользователя и он записывается в словарь
   Он срабатывает на отправку фото от пользователя
       '''


# @dp.message_handler(content_types=['photo'], state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        # Нижеприведенный код использовался для отладки
        # await message.reply(str(data))
        # name_photo = message.caption
        # print(name_photo)
        # current_state = await state.get_state()
        # print(current_state)
        await message.reply('Теперь введи название')


# Ловим второй ответ

# @dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        # current_state = await state.get_state()  -  это для отладки
        # print(current_state)
        await message.reply('Введи описание')

    # Ловим третий ответ


# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажи цену')


# Ловим последнний ответ и обрабатываем полученные данные
''' 
float(message.text)- переводит текст в число с плавающей точкой
await state.finish() - завершает переход по состояниям и бот ВЫХОДИТ из машины состояний
и полностью очищает все записи в словаре. Поэтому эти данные выведем все что получили в чат с пользователем
(str(data)) - это наш словарь приведенный к строке
'''


# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = message.text
            # data['price'] = float(message.text)
        await message.reply(str(data))
        # запускаем функцию добавления в БД Почему state ? Это объект, который содержи текущее состояние – те
        # Все, что ввел модератор -фото, имя, описание, цена
        await sqlite_db.sql_add_command(state)

        await state.finish()


'''
* - означает любое из 4-х сосотояний
два подряд декоратора  - означает срабатывание или первого или второго. (или команда отмена или текст отмена)
второй хэндлер - фильтр текста - игнорирование регистра и юбое состояние
state.get_state() - получаем текущее состояние проверяется на его наличие 
'''


# @dp.message_handler(state="*", commands='отмена')
# @dp.message_handler(Text(equals='отмена', ignore_case=True), state="*")
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('OK')


# Это хэндлер ответа-действий на команду удаления. Подтверждением исполнения колбэка в хэндлере команды Удалить:
# callback_data=f'del {ret[1]}', где {ret[1]} - Название блюда

# @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del'))
"""здесь проверяется - начинается ли сообщение с символов 'del'
    callback_query - имя задаем мы любое
"""


async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")} удалена.', show_alert=True)


'''
   Выполняеся функция из модуля sqlite_db; в нее передается data - это Название блюда
    (replace('del ', '') - заменяет 'del ', на пусто  и таким образом :
    все выражение callback_query.data.replace('del ', '') ==  "Название"
  Администратору передается сообщение в виде алерта
   
  другим вариантом ответа реализации ответа на колбэк - мб :
 bot.answer_callback_query(callback_query.id, text=".......")
'''


# хэндлер команды /Удалить
# @dp.message_handler(commands='Удалить')
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        # создается копия всей БД
        read = await sqlite_db.sql_read2()
        #  перебираем всю БД
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОписание: {ret[2]}\nЦена {ret[-1]}')
            # сначала выбираем очередную выбранную из БД запись
            await bot.send_message(message.from_user.id, text='^^^', reply_markup=InlineKeyboardMarkup().
                                   add(InlineKeyboardButton(f'Удалить {ret[1]}', callback_data=f'del {ret[1]}')))


'''Под каждой записью - в нашем случае под каждым блюдом Меню , Отправляем модератору клавиатуру (которую мы
 создаем прямо здесь) и в ней  Инлайн-кнопку  с текстом text='^^^ - чтобы было  понятно к какому блюду это относится; 
 {ret[1]} - Название;     callback_data=f'del {ret[1]}' - это подтверждение исполнения колбэка и в нем указываем -
    что будем удалять, именно это название БУДЕМ отправлять в БД для удаления - как запрос - и именно его
    будем обрабатывать в @dp.callback_query_handler(lambda x: x.data and x.data.startswith('del'))
    - здесь проверяется - начинается ли сообщение с символов 'del'
'''

# Регистрация созданных хэндлеров
'''
Все вышенаписанное подряд - это если бы мы не работали с модульной структорой Проекта
Поэтому мы должны теперь импортировать написанные хэндлеры в основной модуль main.py
Для этого сначала здесь нужно прописать регистрацию созданных хэндлеров 
А в мейн.пи добавим  admin.register_handlers_admin(dp)
'''


def register_handlers_admin(dp: Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state="*", commands=['отмена'])
    dp.register_message_handler(cancel_handler, Text(equals='отмена', ignore_case=True), state="*")
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_changes_command, commands=['moderator'], is_chat_admin=True)
    dp.register_message_handler(delete_item, commands=['Удалить'])
    dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del'))
