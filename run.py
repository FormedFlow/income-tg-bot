import asyncio
import logging
from routers import router as main_router
from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from config import settings


bot = Bot(token=settings.bot_token)
dp = Dispatcher()

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


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
