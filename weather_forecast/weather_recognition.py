import spacy
import pycountry

from dateparser.search import search_dates

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

    async def __extract_location(self, text):
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

    @staticmethod
    async def __extract_and_translate_time(text):
        base_date = datetime.now()

        parsed_date = search_dates(text, settings={'RELATIVE_BASE': base_date, 'PREFER_DATES_FROM': 'future'})

        if parsed_date is None:
            return str(base_date.date())

        return str(parsed_date[0][1].date())
