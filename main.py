import logging
import tracemalloc
from aiogram import Bot, Dispatcher
from aiogram.types import ContentType

from bot_commands import process_callback_help, \
                         start_command_handler, \
                         help_command_handler, \
                         echo_message

import config
import asyncio

from generate_message import GenerateMessage
from logger_setup import logger_setup

logging.basicConfig(level=logging.ERROR)
logger = logger_setup(__name__)

async def main():
    tracemalloc.start()

    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot)
    generate = GenerateMessage(bot)

    dp.register_callback_query_handler(lambda callback_query: process_callback_help(callback_query, bot))
    dp.register_message_handler(start_command_handler, commands='start')
    dp.register_message_handler(help_command_handler, commands='help')
    dp.register_message_handler(lambda m, g=generate: echo_message(m, g),
                                content_types=ContentType.TEXT)
    
    await dp.start_polling()

if __name__ == '__main__':
    asyncio.run(main())
