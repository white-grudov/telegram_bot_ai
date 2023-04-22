import spacy
import pycountry

from dateparser.search import search_dates

from flashgeotext.geotext import GeoText, GeoTextConfiguration
from flashgeotext.lookup import LookupData, load_data_from_file
from datetime import datetime


class WeatherRecognition:
    LOCATION_NOT_FOUND = 0

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.data = load_data_from_file('./files/cities_data.json')

        lookup = LookupData(name='cities500', data=self.data)
        config = GeoTextConfiguration(**{"use_demo_data": False})
        self.geotext = GeoText(config)
        self.geotext.add(lookup)

    def get_location_date(self, text: str):
        location = self.__extract_location(text)
        if location is None:
            return self.LOCATION_NOT_FOUND, None

        date = self.__extract_and_translate_time(text)
        return location, date

    def __normalize_text(self, text):
        doc = self.nlp(text)

        normalized_tokens = []
        for token in doc:
            if not token.is_stop and not token.is_punct:
                normalized_tokens.append(token.lemma_.lower())

        normalized_text = ' '.join(normalized_tokens)
        return normalized_text

    def __extract_location(self, text):
        results = self.geotext.extract(input_text=self.__normalize_text(text).title(), span_info=True)

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
    def __extract_and_translate_time(text):
        base_date = datetime.now()

        parsed_date = search_dates(text, settings={'RELATIVE_BASE': base_date, 'PREFER_DATES_FROM': 'future'})

        if parsed_date is None:
            return str(base_date.date())

        return str(parsed_date[0][1].date())
