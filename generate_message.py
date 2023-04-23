from logger_setup import logger_setup
from translator import Translator
from weather_forecast.weather_results import get_weather_forecast
from intent_classifier import IntentClassifier

logger = logger_setup(__name__)

tr = Translator()
classifier = IntentClassifier()
classifier.load_model_from_file('./files/intent_classifier.pkl')

def __get_intent(message: str):
    intent = classifier.predict_intent(message)
    return intent

def __generate_message_from_intent(message, intent):
    if intent == 'weather':
        return get_weather_forecast(message)
    else:
        return 'Unrecognized intent'

def generate_message(message: str) -> str:
    try:
        lang, translated = tr.detect_lang_and_translate_to_en(message)
        lang = lang.lower()

        logger.debug(f'Request language: {lang}')
        logger.debug(f'Translated: {translated}')

        intent = __get_intent(translated)
        logger.info(f'Intent: {intent}')
        request_result = __generate_message_from_intent(translated, intent)

        if lang != 'en':
            request_result = tr.translate_to(request_result, lang)
            logger.debug(f'Translated results: {request_result}')
        return request_result
    except Exception as e:
        logger.error(f'Exception: {e}')
        return f'Unexpected error: {e}'