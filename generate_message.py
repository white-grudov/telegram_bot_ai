from aiogram import Bot

from logger_setup import logger_setup
from translator import Translator
from weather_forecast.weather_results import get_weather_forecast
from intent_classifier import IntentClassifier
from image_search.image_search import ImageSearch
from bot_commands import send_text_message, send_image_message, process_summarize

import json

logger = logger_setup(__name__)

class GenerateMessage:
    def __init__(self, bot):
        self.__bot: Bot = bot

        self.__tr = Translator()
        self.__image_search = ImageSearch()
        self.__classifier = IntentClassifier()
        self.__classifier.load_model_from_file('./files/intent_classifier.pkl')

        self.__process_methods = {
            'weather': self.__process_weather_request,
            'image': self.__process_image_request,
            'summarize': self.__process_summary_request
        }

    async def __get_intent(self, message: str):
        intent = await self.__classifier.predict_intent(message)
        return intent

    async def __respond(self, chat_id, message: str):
        await send_text_message(self.__bot, chat_id, message)

    async def __process_weather_request(self, chat_id, message, lang):
        request_result = await get_weather_forecast(message)
        if request_result == 'invalid_location_message':
            with open('./files/messages.json', 'r', encoding='utf-8') as f:
                location_not_found = json.loads(f.read())['invalid_location_message'][lang]
            await self.__respond(chat_id, location_not_found)
            return

        request_result = await self.__tr.translate_from_en(request_result, lang)
        logger.debug(f'Translated results: {request_result}')

        await self.__respond(chat_id, request_result)

    async def __process_image_request(self, chat_id, message, lang):
        query = await self.__image_search.extract_subject(message)
        if query is None:
            with open('./files/messages.json', 'r', encoding='utf-8') as f:
                not_specified_message = json.loads(f.read())['subject_not_specified_message'][lang]
            await self.__respond(chat_id, not_specified_message)
            return

        logger.debug(f'Search subject: {query}')

        with open('./files/messages.json', 'r', encoding='utf-8') as f:
            wait_message = json.loads(f.read())['wait_message'][lang]
        await self.__bot.send_message(chat_id=chat_id, text=wait_message)

        request_url = await self.__image_search.search_image(message)
        if request_url is None:
            with open('./files/messages.json', 'r', encoding='utf-8') as f:
                not_found_message = json.loads(f.read())['image_not_found_message'][lang]
            await self.__respond(chat_id, not_found_message)
            return

        caption = f'Here is the image according to your query <b>"{query}"</b>'
        caption = await self.__tr.translate_from_en(caption, lang)
        logger.debug(f'Caption: {caption}')
        await send_image_message(self.__bot, chat_id, request_url, caption)

    async def __process_summary_request(self, chat_id, message, lang):
        await process_summarize(self.__bot, chat_id, lang)

    async def generate_message(self, chat_id, message: str) -> str:
        try:
            lang, translated = await self.__tr.detect_lang_and_translate_to_en(message)
            logger.debug(f'Request language: {lang}')
            logger.debug(f'Translated: {translated}')

            if lang == 'unknown':
                await self.__respond(chat_id, 'This language is not supported. ' \
                                     'Type /help to see the list of avaiable languages.')
                return

            intent = await self.__get_intent(translated)
            logger.info(f'Intent: {intent}')

            if intent in self.__process_methods:
                await self.__process_methods[intent](chat_id, translated, lang)
            else:
                with open('./files/messages.json', 'r', encoding='utf-8') as f:
                    unrecognized_message = json.loads(f.read())['unrecognized_intent_message'][lang]
                await self.__respond(chat_id, unrecognized_message)

        except Exception as e:
            logger.error(f'Exception: {e}')
            await self.__respond(chat_id, f'Unexpected error: {e}') 