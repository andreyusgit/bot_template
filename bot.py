import logging

from openpyxl import Workbook, load_workbook

from aiogram import Bot, types
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from config import TOKEN
from utils import TestStates
from messages import MESSAGES

logging.basicConfig(format=u'%(filename)+13s [ LINE:%(lineno)-4s] %(levelname)-8s [%(asctime)s] %(message)s',
                    level=logging.DEBUG)

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware()) # все что выше лучше не трогать, только если удалить ненужные библиотеки


@dp.message_handler(commands=['start'])  # эта функция будет выполнена если будет команда "start" в других случаях она не вызывается
async def process_start_command(message: types.Message):
    await message.answer(MESSAGES['start'])


@dp.message_handler(state='*', commands=['help']) # state - эта функция будет выполнена только если пользователь обладает соответсвующем статусом
async def process_help_command(message: types.Message): # '*' - обрабатывает все статусы, если не надо использовать статусы - просто убираем это
    await message.answer(MESSAGES['help'])              # https://mastergroosha.github.io/telegram-tutorial-2/fsm/ - руководство по статусам


@dp.message_handler(state='*', commands=['thanks'])
async def process_help_command(message: types.Message):
    await message.answer(MESSAGES['thx'])


@dp.message_handler(state=TestStates.all()) # как таковой разницы между такой реализацией и state='*' - нету
async def some_test_state_case_met(message: types.Message):
    await message.answer(MESSAGES['no_command'])

# разница между командой выше и командой ниже в том, что верхняя работает, если стоит любой статус, а нижняя - нет статуса вообще

@dp.message_handler() # обрабатывает абсолютно все команды, если они не были обработаны ранее
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, str(msg))


async def shutdown(dispatcher: Dispatcher):
    await dispatcher.storage.close()
    await dispatcher.storage.wait_closed()


if __name__ == '__main__':
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button_1 = types.KeyboardButton(text="/start")  # тут мы делаем кнопку старт, если нужно добавить другие или редактировать эту - нужно посмотреть руководство
    keyboard.add(button_1)                          # https://mastergroosha.github.io/telegram-tutorial-2/buttons/  понятное руководство по кнопкам
    executor.start_polling(dp, on_shutdown=shutdown)
