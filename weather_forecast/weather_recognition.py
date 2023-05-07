import spacy
import pycountry

from dateparser.search import search_dates
from dateparser import parse

from flashgeotext.geotext import GeoText, GeoTextConfiguration
from flashgeotext.lookup import LookupData, load_data_from_file
from datetime import datetime

from text_normalize import normalize

class WeatherRecognition:
    LOCATION_NOT_FOUND = 0

    def __init__(self):
        self.__nlp = spacy.load("en_core_web_sm")
        self.__data = load_data_from_file('./files/cities_data.json')

        lookup = LookupData(name='cities500', data=self.__data)
        config = GeoTextConfiguration(**{"use_demo_data": False})
        self.__geotext = GeoText(config)
        self.__geotext.add(lookup)

    async def get_location_date(self, text: str):
        location = await self.__extract_location(text)
        if location is None:
            return self.LOCATION_NOT_FOUND, None

        date = await self.__extract_and_translate_time(text)
        return location, date

    async def __extract_location(self, text: str):
        normalized_text = await normalize(self.__nlp, text)
        results = self.__geotext.extract(input_text=normalized_text.title(), span_info=True)

        country_code = ''
        for country in pycountry.countries:
            if country.name.lower() in text.lower():
                country_code = f',{country.alpha_2}'
        try:
            city_name = list(results['cities500'].keys())[0]
        except IndexError:
            return None

        return f'{city_name}{country_code}'

    def __extract_date_phrase(self, text):
        doc = self.__nlp(text)
        date_phrases = []
        for token in doc:
            if token.ent_type_ == "DATE" or token.text in ["today", "tomorrow", "week", "before", "after"]:
                date_phrase = token.text
                date_phrases.append(date_phrase)
        return ' '.join(date_phrases)

    async def __extract_and_translate_time(self, text):
        date_str = self.__extract_date_phrase(text)
        base_date = datetime.now()

        parser_date = parse(date_str, settings={'RELATIVE_BASE': base_date, 'PREFER_DATES_FROM': 'future'})
        searched_date = search_dates(date_str, settings={'RELATIVE_BASE': base_date, 'PREFER_DATES_FROM': 'future'})

        if searched_date == None:
            return str(base_date.date())
        elif parser_date == None:
            return 'date_interval_message'
        else:
            return str(parser_date.date())
