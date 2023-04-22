import deepl

from lingua import Language, LanguageDetectorBuilder
from config import DEEPL_API_KEY

LANGUAGES = {
    Language.ENGLISH: 'en-us',
    Language.UKRAINIAN: 'uk',
    Language.POLISH: 'pl',
    Language.SPANISH: 'es',
    Language.GERMAN: 'de',
    Language.FRENCH: 'fr'
}

class Translator:
    def __init__(self):
        self.detector = LanguageDetectorBuilder.from_languages(*LANGUAGES).build()
        self.translator = deepl.Translator(DEEPL_API_KEY)

    def get_language(self, text: str):
        return LANGUAGES[self.detector.detect_language_of(text)]

    def translate_to(self, text: str, lang: str) -> str:
        result = self.translator.translate_text(text, target_lang=lang)
        return result.text


if __name__ == '__main__':
    test = "What will be the weather in Toronto tomorrow?"

    tr = Translator()

    translated_text = tr.translate_to(test, 'en-us')
    print('Translated text:', translated_text)

    original_language = tr.get_language(test)
    print("Original language:", original_language)
