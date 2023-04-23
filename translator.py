import deepl

from config import DEEPL_API_KEY

class Translator:
    def __init__(self):
        self.__translator = deepl.Translator(DEEPL_API_KEY)
    
    def detect_lang_and_translate_to_en(self, text: str) -> tuple[str, str]:
        result = self.__translator.translate_text(text, target_lang='en-us')
        return result.detected_source_lang, result.text

    def translate_to(self, text: str, lang: str) -> str:
        result = self.__translator.translate_text(text, target_lang=lang)
        return result.text


if __name__ == '__main__':
    test = "Jaka pogoda jest w Czarnomorsku?"

    tr = Translator()

    translated_text = tr.translate_to(test, 'en-us')
    print('Translated text:', translated_text)

    lang, translated = tr.detect_lang_and_translate_to_en(test)
    print(f'Detected language: {lang}, translated: {translated}')

    original_language = tr.get_language(test)
    print("Original language:", original_language)
