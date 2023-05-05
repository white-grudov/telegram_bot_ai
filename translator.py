import deepl
import asyncio

from config import DEEPL_API_KEY
from language_classifier import LanguageClassifier

class Translator:
    def __init__(self):
        self.__detector = LanguageClassifier()
        self.__translator = deepl.Translator(DEEPL_API_KEY)

        self.__detector.load_model_from_file('./files/language_classifier.pkl')

    async def detect_lang_from_supported(self, text: str):
        return await self.__detector.predict_language(text)
    
    async def detect_lang_and_translate_to_en(self, text: str) -> tuple[str, str]:
        lang = await self.detect_lang_from_supported(text)
        tr_lang = 'en' if lang == 'en-us' else lang
        if tr_lang == 'unknown':
            result = None
        else:
            result = self.__translator.translate_text(text, source_lang=tr_lang, target_lang='en-us').text
        return lang, result

    async def translate_from_en(self, text: str, lang: str) -> str:
        if lang == 'en-us':
            return text
        result = self.__translator.translate_text(text, source_lang='en', target_lang=lang)
        return result.text

    async def translate_to(self, text: str, lang: str) -> str:
        result = self.__translator.translate_text(text, target_lang=lang)
        return result.text

async def main():
    tr = Translator()

if __name__ == '__main__':
    asyncio.run(main())
