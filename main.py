import logging
import aiogram
from aiogram import Bot, Dispatcher, types

import config as conf
from generate_message import generate_message
from logger_setup import logger_setup

logging.basicConfig(level=logging.ERROR)

logger = logger_setup(__name__)

bot = Bot(token=conf.TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands='start')
async def start_command_handler(message: types.Message):
    await message.answer("Hello! I'm a Telegram bot. Use /help to see what I can do.")

@dp.message_handler(commands='help')
async def help_command_handler(message: types.Message):
    help_text = "Here are the available commands:\n/start - Start the bot\n/help - Get help with using the bot"
    await message.answer(help_text)

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
