import spacy
import asyncio
import re
import requests
import json

from random import randint
from spacy.lang.en.stop_words import STOP_WORDS

from config import GOOGLE_API_KEY, GOOGLE_API_SECRET
from logger_setup import logger_setup

logger = logger_setup(__name__)

class ImageSearch:
    def __init__(self):
        self.__nlp = spacy.load('en_core_web_sm')
        self.__url = "https://www.googleapis.com/customsearch/v1"

    async def extract_subject(self, search_query):
        doc = self.__nlp(search_query)

        noun_phrases = []
        verb_phrases = []
        for chunk in doc.noun_chunks:
            for word in chunk.text.split(' '):
                noun_phrases.append(word)
        for token in doc:
            if token.pos_ in ['NOUN', 'VERB', 'ADJ', 'CONJ']:
                verb = token.text_with_ws + ''.join([child.text_with_ws for child in token.children if child.dep_ in ('advmod', 'acomp', 'attr', 'prep', 'oprd')])
                verb_phrases.append(verb.strip())

        try:
            phrases = noun_phrases + verb_phrases[1:]
            new_phrases = []
            for phrase in phrases:
                words = phrase.split()
                new_phrase = ' '.join([word for word in words if word.lower() not in STOP_WORDS])
                if new_phrase != '' and new_phrase not in new_phrases:
                    new_phrases.append(new_phrase)

            keywords = new_phrases[1:]

            pattern = r"\b(" + "|".join(keywords) + r")\b"
            matches = re.findall(pattern, search_query)
            if not matches:
                return None

            start_pos = search_query.index(matches[0])
            end_pos = search_query.rindex(matches[-1])

            if start_pos == 0:
                return None

            interval = search_query[start_pos:end_pos + len(matches[-1])]
            return interval

        except Exception:
            return None

    @staticmethod
    async def __get_search_params(text: str) -> dict:
        return {
            "key": GOOGLE_API_KEY,
            "cx": GOOGLE_API_SECRET,
            "searchType": "image",
            'q': text,
            'num': 10,
            'save': 'active',
            'fileType': 'jpg'
        }

    async def search_image(self, text: str):
        response = requests.get(self.__url, params=await self.__get_search_params(text))
        data = json.loads(response.text)
        if 'items' not in data:
            return None

        image_url = data["items"][randint(1, min(10, len(data['items']) - 1))]["link"]
        return image_url

async def main():
    query = 'Give me an image of cute cat'

    image_search = ImageSearch()
    processed_request = image_search.extract_subject(query)
    print(await image_search.search_image(processed_request))

if __name__ == '__main__':
    asyncio.run(main())