import logging
import aiogram
from aiogram import Bot, Dispatcher, types

from bot_commands import process_callback_button, start_command_handler, help_command_handler

import config as conf
from generate_message import generate_message
from logger_setup import logger_setup

logging.basicConfig(level=logging.ERROR)

logger = logger_setup(__name__)

bot = Bot(token=conf.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

dp.register_callback_query_handler(lambda callback_query: process_callback_button(callback_query, bot))
dp.register_message_handler(start_command_handler, commands='start')
dp.register_message_handler(help_command_handler, commands='help')

@dp.message_handler(content_types=types.ContentType.TEXT)
async def echo_message(message: types.Message):
    if message.chat.type == 'group':
        if conf.USERNAME not in message.text:
            return
        else:
            logger.debug(f'Message from a group {message.chat.title} ({message.chat.id})')
            input_message = message.text.replace(conf.USERNAME, '')
    else:
        logger.debug(f'Message from a user {message.chat.first_name} {message.chat.last_name} {message.chat.username}'
                     f' ({message.chat.id})')
        input_message = message.text

    logger.info(f'Message text: {input_message}')
    result = generate_message(input_message)

    logger.info(f'Request result: {result}')
    await message.answer(result)


if __name__ == '__main__':
    aiogram.executor.start_polling(dp, skip_updates=True)
