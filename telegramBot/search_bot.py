import asyncio
import json
import os

from aiogram import types, Dispatcher, executor, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from main import add_sub_list,check_sub_list,del_sub, get_last_announ, check_new_update
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types


storage = MemoryStorage()
bot = Bot(token=os.environ["TOKEN"], parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=storage)

class FSMstart(StatesGroup):
    sending_userid = State()

class FSMadd(StatesGroup):
    sending_keyword = State()

class FSMdel(StatesGroup):
    sending_keyword = State()

class FSMwork(StatesGroup):
    sending_annonce = State()


#########################################################################################################
@dp.message_handler(commands="start", state=None)
async def start(message:types.Message):
    await message.answer("add - Add product subscription "
                         "\ndel - Delete product subscription"
                         "\nstart - Start subscriptions"
                         "\nstop - Stop subscriptions"
                         "\nmy_subs - My subscriptions"
                         )
    await message.answer("Enter your telegram id:")
    await FSMstart.sending_userid.set()


@dp.message_handler(content_types=["text"], state=FSMstart.sending_userid)
async def set_id(message: types.Message, state: FSMContext):
    os.environ["USER_ID"] = message.text
    await message.reply("Done!")
    await state.finish()

#########################################################################################################


# @dp.message_handler(commands="", state=None)
# async def cm_add(message: types.Message):
#     await FSMadd.sending_keyword.set()
#     await message.answer("Add search keywords:")
#
#
# @dp.message_handler(content_types=["text"], state=FSMadd.sending_keyword)
# async def set_keyword(message: types.Message, state: FSMContext):
#     add_sub_list(message.text)
#     await message.reply("Done!")
#     await state.finish()

#########################################################################################################


# @dp.message_handler(commands="del", state=None)
# async def cm_del(message: types.Message):
#     if not check_sub_list():
#         await message.answer("Your sublist is empty, use the 'add' command to add the keywords")
#     else:
#         await message.answer("Choose a keyword:")
#         await FSMdel.sending_keyword.set()
#         await message.answer(check_sub_list())
#
#
# @dp.message_handler(content_types=["text"], state=FSMdel.sending_keyword)
# async def set_keyword(message:types.Message, state: FSMContext):
#     await message.answer(f"{del_sub(message.text.lower())} keywords delete")
#     await state.finish()

#########################################################################################################


@dp.message_handler(commands="check_all_borrowings")
async def check_all_borrowing(message:types.Message):
        await message.answer(check_all_borrowing())

#########################################################################################################

# @dp.message_handler(commands="stop_subs")
# async def start_subs(message:types.Message):
#         await message.answer("stop tracking subscriptions")
#         config.wait_mode = False

#########################################################################################################


@dp.message_handler(commands="track_subs", state=None)
async def start_subs(message:types.Message):

        with open("subs.json") as file:
            data = json.load(file)
            if len(data['key']) >= 1:
                await message.answer("start tracking subscriptions....")
                loop = asyncio.get_event_loop()
                loop.create_task(check_update_every())
                await FSMwork.sending_annonce.set()
                for sub_word in data["key"]:
                    get_last_announ(sub_word)
            else:
                await message.answer("Before you start tracking, use the 'add' command to add the keywords")


async def check_update_every():

        with open("subs.json") as file:
            data = json.load(file)
            while len(data['key']) >= 1:
                for sub_word in data["key"]:
                    answer = check_new_update(sub_word)
                    for key, item in answer.items():
                        await bot.send_message(os.environ["USER_ID"], f"{item['link']}")
                await asyncio.sleep(20)


@dp.message_handler(commands='stop_subs', state=FSMwork.sending_annonce)
async def set_keyword(message:types.Message, state: FSMContext):
    await message.answer("stop tracking subscriptions")
    await state.finish()


def main():
    executor.start_polling(dp)


if __name__ == "__main__":
    main()

