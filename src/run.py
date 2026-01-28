import asyncio
import logging
from routers import router as main_router
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from core.config import base_settings

from middlewares.middlewares import DBSessionMiddleware
from core.database import async_seshmaker


bot = Bot(token=base_settings.bot_token)
dp = Dispatcher()

dp.message.middleware(DBSessionMiddleware(async_seshmaker))
dp.callback_query(DBSessionMiddleware(async_seshmaker))

dp.include_router(main_router)

async def main():
    await dp.start_polling(bot)


# @dp.message(CommandStart())
# async def start(message: Message):
#     if message.text:
#         await message.reply(message.text)
#     elif message.sticker:
#         await message.reply_sticker(message.sticker.file_id)


@dp.message(Command('help'))
async def handle_help(message: Message):
    await message.answer("I'm just an echo bot")

@dp.message(Command('test'))
async def test_user_id(message: Message):
    await message.answer(str(message.from_user.id))


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
