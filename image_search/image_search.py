import spacy
import random
import asyncio
from google_images_search import GoogleImagesSearch
from spacy.lang.en.stop_words import STOP_WORDS

from config import GOOGLE_API_KEY, GOOGLE_API_SECRET
from text_normalize import normalize
from logger_setup import logger_setup

logger = logger_setup(__name__)

class ImageSearch:
    def __init__(self):
        self.__nlp = spacy.load('en_core_web_sm')
        self.__gis = GoogleImagesSearch(GOOGLE_API_KEY, GOOGLE_API_SECRET)

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
                
            start_index = search_query.find(keywords[0])
            end_index = search_query.find(keywords[-1]) + len(keywords[-1])

            interval = search_query[start_index:end_index]
            return interval
        
        except IndexError:
            return None

    async def __get_search_params(self, text: str) -> dict:
        return {
            'q': text,
            'num': 10,
            'save': 'active',
            'fileType': 'jpg'
        }

    async def search_image(self, text: str):
        self.__gis.search(await self.__get_search_params(text))
        results = self.__gis.results()
        if len(results) == 0:
            return None
        result = random.choice(results)
        return result.url

async def main():
    query = 'Give me an image of cute cat'
    
    image_search = ImageSearch()
    print(await image_search.search_image(query))

if __name__ == '__main__':
    asyncio.run(main)