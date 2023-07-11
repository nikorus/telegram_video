from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

import os
from dotenv import load_dotenv
load_dotenv()  # This reads the environment variables inside .env

token = os.getenv('TOKEN')
# инициализируем бот
bot = Bot(token)
# инициализируем диспетчер передавая в него экземпляр бота
dp = Dispatcher(bot)


@dp.message_handler()
# декорируемая ф-я
async def echo_send(message: types.Message):  # имя функции любое
    await message.answer(message.text)  # 1-й способ
    # await message.reply(message.text)  # 2-й способ тоже, о с повторением исходного сообщения
    # await bot.send_message(message.from_user.id, message.text)  #3-й способ - только если пользователь уже обращался к боту

# запуск бота с параметром пропускать обновления - все сообщения которые приходят боту в офлайн
executor.start_polling(dp, skip_updates=True)
