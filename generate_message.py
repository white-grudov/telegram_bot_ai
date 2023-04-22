from logger_setup import logger_setup
from translator import Translator
from weather_forecast.weather_results import get_weather_forecast
from intent_classifier import IntentClassifier

logger = logger_setup(__name__)

tr = Translator()
classifier = IntentClassifier()
classifier.load_model_from_file('./files/intent_classifier.pkl')

def get_intent(message: str):
    intent = classifier.predict_intent(message)
    return intent

def generate_message_from_intent(message, intent):
    if intent == 'weather':
        return get_weather_forecast(message)
    else:
        return 'Unrecognized intent'

def generate_message(message: str) -> str:
    try:
        lang = tr.get_language(message)
        logger.debug(f'Request language: {lang}')
        translated = tr.translate_to(message, 'en')
        logger.debug(f'Translated: {translated}')

        intent = get_intent(translated)
        logger.info(f'Intent: {intent}')
        request_result = generate_message_from_intent(translated, intent)

        translated_result = tr.translate_to(request_result, lang)
        logger.debug(f'Translated results: {translated_result}')
        return translated_result
    except Exception as e:
        logger.error(f'Exception: {e}')
        return f'Unexpected error: {e}'