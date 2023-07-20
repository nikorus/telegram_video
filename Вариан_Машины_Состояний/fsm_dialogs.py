import os
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage

''' импортируется обычная клавиатура и кнопки'''
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Импортируем класс который позволяет читать сообщения пользователя
from aiogram.dispatcher.filters import Text

# создаем экземпляр класса
storage = MemoryStorage()

from aiogram.dispatcher.filters.state import State, StatesGroup

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher, FSMContext
from dotenv import load_dotenv

load_dotenv()  # This reads the environment variables inside .env
token = os.getenv('TOKEN')
# инициализируем бот
bot = Bot(token)
# инициализируем диспетчер передавая в него экземпляр бота
# dp = Dispatcher(bot)
#  добавляем параметр бота, где будет хранится информация
dp = Dispatcher(bot=bot, storage=storage)

''' Функция выдает клавиатуру'''


def get_keyboard() -> ReplyKeyboardMarkup:
    # создаем экземпляр класса клавиатуры
    kb = ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add(KeyboardButton('Начать_работу'))  # добавляется 1 кнопка

    return kb


# Создадаим пользовательску клавиатуру для отмены действий по состояним - сбросить их
def get_cancel() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton('/cancel'))


# Создаем класс состояний Бота, который наследуется от класса StatesGroup
# и в этом классе создаем 2 состояния
class clientStatesGroup(StatesGroup):
    photo = State()
    desc = State()


@dp.message_handler(commands=['start'])
async def cmd_start(message: types.Message) -> None:
    # передает пользовательскую клавиатуру  и вызывает ф-ю
    await message.answer('Добро пожаловать', reply_markup=get_keyboard())
    await message.delete()


# обработка команды пользователя по отмене - сначала проверяется находится ли Бот в одном из состояний
# state='*' -все состояния
@dp.message_handler(commands=['cancel'], state='*')
async def cmd_start(message: types.Message, state: FSMContext) -> None:
    current_state = await state.get_state()
    if current_state is None:
        return
    await message.reply('Ваше действие отменено', reply_markup=get_keyboard())  # Возвращаем клавиатуру после отмены
    await state.finish()


# Обработаем сообщение от пользователя ( НЕ КОМАНДУ)
@dp.message_handler(Text(equals='Начать_работу', ignore_case=True), state=None)
async def start_work(message: types.Message) -> None:
    await clientStatesGroup.photo.set()  # Устанавливаем состояние photo и передадим клавиатуру
    await message.answer('Сначала отправь нам фото', reply_markup=get_cancel())


# Проверяем является ли фотографией то, что отправил пользователь
# ставим фильтр
@dp.message_handler(lambda message: not message.photo, state=clientStatesGroup.photo)
async def check_photo(message: types.Message):
    return await message.reply('Это не фотография!')


# Теперь обработаем пришедшее фото
@dp.message_handler(lambda message: message.photo, content_types=['photo'], state=clientStatesGroup.photo)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:  # стандартная процедура для сохранения в MemoryStorage в словаре , имя даем мы
        # message.photo - это фото отправленное пользователем, 'photo' - это ключь по которому запишется file_id фото
        data['photo'] = message.photo[0].file_id
        # изменяем состояние бота на следующее
    await clientStatesGroup.next()
    await message.reply('А теперь отправь нам описание фото')


# Теперь обработаем пришедшее описание
@dp.message_handler(state=clientStatesGroup.desc)
async def load_photo(message: types.Message, state: FSMContext):
    async with state.proxy() as data:  # стандартная процедура для сохранения в MemoryStorage в словаре , имя даем мы
        # message.photo - это фото отправленное пользователем, 'photo' - это ключь по которому запишется file_id фото
        data['desc'] = message.text
        # изменяем состояние бота на финиш

    await message.reply('Ваше фото сохранено')
    # обратимся к менеджеру контекста и выведем
    async with state.proxy() as data:
        #print(data)  - это выводв консоль для отладки
        await bot.send_photo(chat_id=message.from_user.id, photo=data['photo'], caption=data['desc'])
    await state.finish()

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
