import logging
import aiogram
from aiogram import Bot, Dispatcher
from aiogram.types import Message, ContentType

from bot_commands import process_callback_help, \
                         start_command_handler, \
                         help_command_handler

import config
from generate_message import GenerateMessage
from logger_setup import logger_setup

logging.basicConfig(level=logging.ERROR)
logger = logger_setup(__name__)

bot = Bot(token=config.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)
generate = GenerateMessage(bot)

dp.register_callback_query_handler(lambda callback_query: process_callback_help(callback_query, bot))
dp.register_message_handler(start_command_handler, commands='start')
dp.register_message_handler(help_command_handler, commands='help')

@dp.message_handler(content_types=ContentType.TEXT)
async def echo_message(message: Message):
    if message.chat.type == 'group':
        if config.USERNAME not in message.text:
            return
        else:
            logger.debug(f'Message from a group {message.chat.title} ({message.chat.id})')
            input_message = message.text.replace(config.USERNAME, '')
    else:
        logger.debug(f'Message from a user {message.chat.first_name} {message.chat.last_name} '
                     f'{message.chat.username} ({message.chat.id})')
        input_message = message.text

    logger.info(f'Message text: {input_message}')

    await generate.generate_message(message.chat.id, input_message)

if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
