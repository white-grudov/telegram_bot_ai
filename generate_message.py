from logger_setup import logger_setup
from translator import Translator
from weather_forecast.weather_results import get_weather_forecast
from intent_classifier import IntentClassifier
from image_search.image_search import ImageSearch
from bot_commands import send_text_message, send_image_message

logger = logger_setup(__name__)

class GenerateMessage:
    def __init__(self, bot):
        self.__bot = bot

        self.__tr = Translator()
        self.__image_search = ImageSearch()
        self.__classifier = IntentClassifier()
        self.__classifier.load_model_from_file('./files/intent_classifier.pkl')

    def __get_intent(self, message: str):
        intent = self.__classifier.predict_intent(message)
        return intent

    async def __respond(self, chat_id, message: str):
        await send_text_message(self.__bot, chat_id, message)

    async def __process_weather_request(self, chat_id, message, lang):
        if lang == 'unknown':
            await self.__respond(chat_id, 'This language is not supported')

        request_result = get_weather_forecast(message)
        request_result = self.__tr.translate_from_en(request_result, lang)
        logger.debug(f'Translated results: {request_result}')

        await self.__respond(chat_id, request_result)

    async def __process_image_request(self, chat_id, message, lang):
        query = self.__image_search.extract_subject(message)
        if query is None:
            await self.__respond(chat_id, 'The search subject is not specified')

        logger.debug(f'Search subject: {query}')

        request_url = self.__image_search.search_image(message)
        if request_url is None:
            self.__respond(chat_id, self.__tr.translate_from_en(
                'Unfortunately, the image was not found. Please try another request'))

        caption = f'Here is the image according to your query <b>"{query}"</b>'
        caption = self.__tr.translate_from_en(caption, lang)
        logger.debug(f'Caption: {caption}')
        await send_image_message(self.__bot, chat_id, request_url, caption)

    async def generate_message(self, chat_id, message: str) -> str:
        try:
            lang, translated = self.__tr.detect_lang_and_translate_to_en(message)
            logger.debug(f'Request language: {lang}')
            logger.debug(f'Translated: {translated}')

            intent = self.__get_intent(translated)
            logger.info(f'Intent: {intent}')

            if intent == 'weather':
                await self.__process_weather_request(chat_id, translated, lang)
            elif intent == 'image':
                await self.__process_image_request(chat_id, translated, lang)
            else:
                await self.__respond(chat_id, 'Unrecognized intent')

        except Exception as e:
            logger.error(f'Exception: {e}')
            await self.__respond(chat_id, f'Unexpected error: {e}') 