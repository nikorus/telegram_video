from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher.filters.state import State, StatesGroup
from create_bot import dp, bot

# В хэндлерах commands  - это обработка команд, те пользователь вводит / перед текстом

ID = None
'''
Создаем класс состояний  с любым именем , который наследуется от базового класса StatesGroup 
 в нем будет 4 состояния photo - для подгрузки меню; = State() - указывается что это будет именно сосотояние
name - назвыание блюда  description - описание price - цена 
Этот ласс  нужен, чтобы бот переходил между состояниями  по  заданном нами алгоритме 
Порядок записи определяет последовательность состояний. по которому можно двигаться
так :   await FSMAdmin.next()
'''

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()


'''
Доступ к командам админа дб только у администратора. Для этого нужно сделать праверку на администратора
Это можно делать различными фильтрами, а можно - если бот добавлен в группу - т.е. он администрирует группу
Тогда проверку можно сделать только проверяя - является ли клиент Администратором группы
Причем , админнистратор должен написать команду НЕ БОТУ а В ГРУППУ
ВО ВСЕХ хэндлерах нужно добавить проверку на админа:
if message.from_user.id == ID:
'''

# Получаем ID текущего модератора
# is_chat_admin=   - это фильтр
# @dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_changes_command(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Что будем делать шеф ?')  # , reply_markup=button_case_admin
    # - это потом добавим клавиатуру админу
    await message.delete()


'''
Ниже расположен Базовый хендлер, который запускает машину состояний. Это все для администратора. state=None - потому
что это начальный хэндлер старта и Машина старта не имеет сосотояния; функция - cm_start - любое имя
FSMAdmin.photo.set() - запускаем созданный экземпляр класса, в котором есть метод photo и даем set() - установить
состояние машины.  даем ему сообщение - загрузить фото
Как только админ напишет Загрузить, срабатывает данный хэндлер и машина переходит в режим СОСТОЯНИЕ = photo 
'''

# Начало диалога загрузки нового пункта Меню

# @dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message: types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Загрузи фото')

    # Ловим первый ответ и пишем его в словарь
    '''
    После перехода машины в состояние фото : Здесь отлавливается первый ответ пользователя и он записывается в словарь
   Он срабатывает на отправку фото от пользователя
    state=FSMAdmin.photo - бак бот понимает что сюда приходит  первый ответ от пользователя
    content_types=['photo'] - будем отправлять картинку с пиццей
    load_photo(m - имя любое, state: FSMContext - параметр с аннотацией, он возможен так как мы его ранее импортировали
    из aiogram
    полученное фото от пользователя сохраняется в словаре машины сосотояния
    реализовать это в коде можно 3 способами .   with state.proxy() as data: - это самый оптимальный
    state.proxy() - это словарь, он открывается с именем  data. В него записывается с ключом 'photo'
    data['photo'] = message.photo[0].file_id
    Вся картинка не записывается тк у Телеграм есть фича - каждому отправленному файлу присваивать уникальный номер -
    message.photo[0].file_id
    К словарю можно обращаться и методами словарей, но они не выкидывают ошибок если что то записали неверно
   Мы этот номер записываем в базу данных и пользователю отправляется картинка по этому file_id
    Поскольку ответ на 1-й вопрос от пользователя получен - то оператором FSMAdmin.next() - переводим наш бот
    в сосотояние ожидания слледующего ответа и отправляем ему следующее задание -message.reply('Теперь введи название')
    cancel_handler -
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
'''await FSMAdmin.next() - перевело бот в ожидание следующего ответа - те он находится в состоянии name
(state=FSMAdmin.name) - это значит, что эта функция будет выполняться когда бот будет в сосотоянии name
 state.proxy() as data: - открываем словарь с именем дата и в него под ключем data['name'] = записываем message.text
await FSMAdmin.next() - переход бота в следующее состояние - description
message.reply('Введи описание') - выводится сообщение пользователю
'''

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
''' все аналогично со вторым
await FSMAdmin.next() - перводит в следующее сосотояние price
'''

# @dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await message.reply('Теперь укажи цену')

# Ловим последнний ответ и обрабатываем полученные данные
''' все аналогично с предъидущими
float(message.text)- переводит текст в число с плавающей точкой
await state.finish() - завершает переход по состояниям и бот ВЫХОДИТ из машины состояний
и полностью очищает все записи в словаре. Поэтому эти данные надо или обработать или сохранить.Существует несколько 
вариантов этого. Самый простой - для демонстрации вывести все что получили в чат с пользователем
    async  with state.proxy() as data: открываем наш словарь
        await message.reply(str(data)) выводим в сообщение с полученными ответами пользователя
(str(data)) - это наш словарь приведенный к строке
Обычно же используется БД (это будет рассмотрено позднее)
'''

# @dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['price'] = float(message.text)

        async with state.proxy() as data:
            await message.reply(str(data))
        await state.finish()

'''
Смысл двух подряд декораторов - первый реагирует на простой текст отмена, а второй на команду /отмена
* - означает любое из 4-х сосотояний
два подряд декоратора  - означает срабатывание или первого или второгоили команда отмена или текст
второй хэндлер - фильтр текста - игнорирование регистра и юбое состояние
state.get_state() - получаем текущее состояние проверяется на его наличие 
если его нет - то возвращается НИКАКОЙ . А если состояние есть - то осуществляется
переход в состояние финишь - выход из машины состояния
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


# Регистрация созданных хэндлеров
'''
Все вышенаписанное подряд - это если бы мы не работали с модульной структорой Проекта
Поэтому мы должны теперь импортировать написанные хэндлеры в основной модуль main.py
Для этого сначала здесь нужно прописать регистрацию созданных хэндлеров типа как мы это сделали
в клиен.пи
def register_handlers_client(dp : Dispatcher):  и тд
по сути все написанные декораторы ПЕРЕНОСЯТСЯ в операторы
dp.register_message_handler(cm_start, commands=['Загрузить'])  и тд
Поэтому ВВЕРХУ эти декораторы можно убрать, но мы их акомментируем для наглядности в мейн.пи добавим
 admin.register_handlers_admin(dp)
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
