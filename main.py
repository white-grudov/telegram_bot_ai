import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3' 

import logging
import tracemalloc

from aiogram import Bot, Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.types import ContentType
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from bot_commands import process_callback_help, \
                         start_command_handler, \
                         help_command_handler, \
                         process_request, \
                         process_text, \
                         TextInputState

import config
import asyncio

from generate_message import GenerateMessage
from logger_setup import logger_setup

logging.basicConfig(level=logging.INFO)
logger = logger_setup(__name__)

async def main():
    tracemalloc.start()

    bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
    dp = Dispatcher(bot, storage=MemoryStorage())
    dp.middleware.setup(LoggingMiddleware())
    generate = GenerateMessage(bot)

    dp.register_callback_query_handler(lambda callback_query: process_callback_help(callback_query, bot))
    dp.register_message_handler(start_command_handler, commands='start')
    dp.register_message_handler(help_command_handler, commands='help')
    dp.register_message_handler(lambda m, g=generate: process_request(m, g),
                                content_types=ContentType.TEXT)
    dp.register_message_handler(process_text, 
                                lambda message: message.text, 
                                state=TextInputState.waiting_for_text)
    
    logger.info('The bot is starting...')
    try:
        await dp.start_polling()
    finally:
        await bot.session.close()

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        pass
    except RuntimeError as e:
        if str(e) != 'Event loop is closed':
            raise e
