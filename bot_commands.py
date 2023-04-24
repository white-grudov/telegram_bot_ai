from aiogram import Bot
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import Message, CallbackQuery

from translator import Translator

tr = Translator()

languages = ['en-us', 'uk', 'pl', 'es', 'de', 'fr']
cities = {
    'en-us': 'London',
    'uk': 'Kyiv',
    'pl': 'Warsaw',
    'es': 'Barcelona',
    'de': 'Berlin',
    'fr': 'Paris'
}
buttons = [
    InlineKeyboardButton('🇬🇧', callback_data=languages[0]),
    InlineKeyboardButton('🇺🇦', callback_data=languages[1]),
    InlineKeyboardButton('🇵🇱', callback_data=languages[2]),
    InlineKeyboardButton('🇪🇸', callback_data=languages[3]),
    InlineKeyboardButton('🇩🇪', callback_data=languages[4]),
    InlineKeyboardButton('🇫🇷', callback_data=languages[5]),
]

def get_help_message(lang: str) -> str:
    return f'''This is a AI chat bot which can execute commands by recognizing the human language.

Current features:

☀️ Weather forecast
Type your request by specifying the location and date (if no date specified, the forecast for today will be given). Example request:
"What is the weather in {cities[lang]} now?"

🏗 Other features under construction...

Press the buttons below to view this message in one of supported languages.'''

async def process_callback_help(callback_query: CallbackQuery, bot: Bot):
    if not callback_query.data in languages:
        return

    keyboard = InlineKeyboardMarkup(row_width=6).add(*buttons)

    await bot.edit_message_text(
        chat_id=callback_query.message.chat.id,
        message_id=callback_query.message.message_id,
        text=tr.translate_to(get_help_message(callback_query.data), callback_query.data),
        reply_markup=keyboard,
    )

async def start_command_handler(message: Message):
    await message.answer("Hello! I'm a Telegram bot. Use /help to see what I can do.")

async def help_command_handler(message: Message):
    keyboard = InlineKeyboardMarkup(row_width=6).add(*buttons)
    await message.answer(get_help_message('en-us'), reply_markup=keyboard)