import spacy
import pycountry

from dateparser.search import search_dates
from geotext import GeoText

from flashgeotext.geotext import GeoText, GeoTextConfiguration
from flashgeotext.lookup import LookupData, load_data_from_file
from nltk.corpus import wordnet as wn
from datetime import datetime


class WeatherRecognition:
    WEATHER_NOT_RELATED = 0
    LOCATION_NOT_FOUND = 1

    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.data = load_data_from_file('./files/cities_data.json')
        self.weather_words = {"weather", "forecast"}
        self.weather_verbs = {"rain", "shine", "snow", "pour", "storm"}
        self.weather_adjectives = {"sunny", "rainy", "foggy", "cloudy", "windy", "stormy", "snowy", "hot", "cold"}
        self.ambiguous_words = {"rain", "snow", "storm"}

        lookup = LookupData(name='cities500', data=self.data)
        config = GeoTextConfiguration(**{"use_demo_data": False})
        self.geotext = GeoText(config)
        self.geotext.add(lookup)

    def get_location_date(self, text: str):
        if not self.__is_weather_related(text):
            return self.WEATHER_NOT_RELATED, None

        location = self.__extract_location(text)
        if location is None:
            return self.LOCATION_NOT_FOUND, None

        date = self.__extract_and_translate_time(text)
        return location, date

    def __is_weather_related(self, text: str) -> bool:
        doc = self.nlp(text)
        weather_synsets = set(wn.synset("weather.n.01").closure(lambda s: s.hyponyms()))

        weather_score = 0
        for token in doc:
            synsets = wn.synsets(token.text)
            for synset in synsets:
                if synset in weather_synsets:
                    weather_score += 1
                    break
                for lemma in synset.lemmas():
                    if lemma.name() in self.weather_words:
                        weather_score += 1
                        break
                    if lemma.name() in self.weather_verbs and token.pos_ == "VERB":
                        weather_score += 1
                        break
                    if lemma.name() in self.weather_adjectives and token.pos_ == "ADJ":
                        weather_score += 1
                        break
                    if lemma.name() in self.ambiguous_words:
                        if token.dep_ == "nsubj" and token.head.lemma_ in self.weather_verbs:
                            weather_score += 1
                            break
                        elif token.head.dep_ == "nsubj" and token.head.head.lemma_ in self.weather_verbs:
                            weather_score += 1
                            break

        if weather_score > 0:
            return True
        else:
            return False

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
