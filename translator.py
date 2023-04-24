import deepl

from lingua import Language, LanguageDetectorBuilder
from config import DEEPL_API_KEY

from language_classifier import LanguageClassifier

LANGUAGES = {
    Language.ENGLISH: 'en',
    Language.UKRAINIAN: 'uk',
    Language.POLISH: 'pl',
    Language.SPANISH: 'es',
    Language.GERMAN: 'de',
    Language.FRENCH: 'fr'
}

class Translator:
    def __init__(self):
        self.__detector = LanguageClassifier().load_model_from_file('./files/language_classifier.pkl')
        self.__translator = deepl.Translator(DEEPL_API_KEY)

    def detect_lang_from_supported(self, text: str):
        return LANGUAGES[self.__detector.detect_language_of(text)]
    
    def detect_lang_and_translate_to_en(self, text: str) -> tuple[str, str]:
        result = self.__translator.translate_text(text, target_lang='en-us')
        return result.detected_source_lang, result.text

    def translate_to(self, text: str, lang: str) -> str:
        result = self.__translator.translate_text(text, target_lang=lang)
        return result.text
    
    @property
    def supported_languages(self):
        return LANGUAGES.values()


if __name__ == '__main__':
    test = "Jaka pogoda jest w Czarnomorsku?"

    tr = Translator()

    translated_text = tr.translate_to(test, 'en-us')
    print('Translated text:', translated_text)

    lang, translated = tr.detect_lang_and_translate_to_en(test)
    print(f'Detected language: {lang}, translated: {translated}')

    original_language = tr.detect_lang_from_supported(test)
    print("Original language:", original_language)
