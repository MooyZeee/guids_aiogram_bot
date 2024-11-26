from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.methods import DeleteWebhook
from aiogram.types import BotCommandScopeAllPrivateChats
from aiogram import Bot, Dispatcher

import asyncio
import logging

from auxiliary_commands.stated_bot_commands import private
from handlers.handler import router
from config.config import TOKEN


async def main():
    bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher()
    dp.include_router(router)
    await bot.set_my_commands(commands=private, scope=BotCommandScopeAllPrivateChats())
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, skip_updates=True)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')










































