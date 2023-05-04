from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery

import json
from translator import Translator
from logger_setup import logger_setup

logger = logger_setup(__name__)

tr = Translator()

languages = ['en-us', 'uk', 'pl', 'es', 'de', 'fr']

buttons = [
    InlineKeyboardButton('🇬🇧', callback_data=languages[0]),
    InlineKeyboardButton('🇺🇦', callback_data=languages[1]),
    InlineKeyboardButton('🇵🇱', callback_data=languages[2]),
    InlineKeyboardButton('🇪🇸', callback_data=languages[3]),
    InlineKeyboardButton('🇩🇪', callback_data=languages[4]),
    InlineKeyboardButton('🇫🇷', callback_data=languages[5]),
]

def get_help_message(lang: str) -> str:
    with open('./files/messages.json', 'r', encoding='utf-8') as f:
        return json.loads(f.read())['help_message'][lang]

async def process_callback_help(callback_query: CallbackQuery, bot: Bot):
    if not callback_query.data in languages:
        return

    keyboard = InlineKeyboardMarkup(row_width=6).add(*buttons)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=get_help_message(callback_query.data),
        reply_markup=keyboard,
        parse_mode='html'
    )

async def start_command_handler(message: Message):
    await message.answer("Hello! I'm a Telegram bot. Use /help to see what I can do.")

async def help_command_handler(message: Message):
    keyboard = InlineKeyboardMarkup(row_width=6).add(*buttons)
    await message.answer(get_help_message('en-us'), reply_markup=keyboard, parse_mode='html')

async def send_text_message(bot: Bot, chat_id: str, text: str):
    logger.info(f'Request result: {text}')
    await bot.send_message(chat_id=chat_id, text=text)

async def send_image_message(bot: Bot, chat_id: str, image_url: str, caption=None):
    logger.info(f'Request image url: {image_url}')
    await bot.send_photo(chat_id=chat_id, photo=image_url, caption=caption, parse_mode='html')