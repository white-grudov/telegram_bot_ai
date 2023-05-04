import spacy
import random
from google_images_search import GoogleImagesSearch

from config import GOOGLE_API_KEY, GOOGLE_API_SECRET
from text_normalize import normalize
from logger_setup import logger_setup

logger = logger_setup(__name__)

class ImageSearch:
    def __init__(self):
        self.__nlp = spacy.load('en_core_web_sm')
        self.__gis = GoogleImagesSearch(GOOGLE_API_KEY, GOOGLE_API_SECRET)

    def extract_subject(self, search_query):
        doc = self.__nlp(search_query)
        noun_chunks = list(doc.noun_chunks)
        if noun_chunks:
            return ' '.join(noun_chunk.text for noun_chunk in noun_chunks[1:])
        return None

    def __get_search_params(self, text: str) -> dict:
        return {
            'q': text,
            'num': 10,
            'save': 'active',
            'fileType': 'jpg'
        }

    def search_image(self, text: str):
        self.__gis.search(self.__get_search_params(text))
        results = self.__gis.results()
        if len(results) == 0:
            return None
        result = random.choice(results)
        return result.url

if __name__ == '__main__':
    query = 'Give me an image of cute cat'
    
    image_search = ImageSearch()
    print(image_search.search_image(query))