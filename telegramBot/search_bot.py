from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import Message
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.utils import executor

from telegramBot.main import (
    check_all_borrowing,
    check_new_update,
    check_unpaid_borrowing,
)

storage = MemoryStorage()
bot = Bot(token=TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)


class FSMstart(StatesGroup):
    sending_userid = State()


class FSMadd(StatesGroup):
    sending_keyword = State()


class FSMdel(StatesGroup):
    sending_keyword = State()


class FSMwork(StatesGroup):
    sending_annonce = State()


@dp.message_handler(commands="start", state=None)
async def start(message: types.Message):
    await message.answer("Welcome to the best library")


@dp.message_handler(commands="check_all_borrowing")
async def check_borrowing(message: types.Message):
    await message.answer(check_all_borrowing())


@dp.message_handler(commands="check_updates")
async def update(message: types.Message):
    await message.answer(check_new_update())


@dp.message_handler(commands="unpaid_borrowings")
async def update(message: types.Message):
    await message.answer(check_unpaid_borrowing())


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
