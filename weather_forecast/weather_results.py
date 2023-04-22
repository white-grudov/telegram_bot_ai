import pycountry
from logger_setup import logger_setup

from weather_forecast.weather_recognition import WeatherRecognition
from weather_forecast.weather_requests import generate_weather_forecast

location_not_found = 'The location specified does not exist'

logger = logger_setup(__name__)

wr = WeatherRecognition()

def get_weather_forecast(message: str):
    try:
        location, date = wr.get_location_date(message)

        if location == WeatherRecognition.LOCATION_NOT_FOUND:
            logger.info('Location is invalid')
            return location_not_found
        logger.debug(f'Extracted data: {location}, {date}')

        weather_request_result = generate_weather_forecast(location, date)
        split_location = location.split(',')
        if len(split_location) > 1:
            country_code = split_location[1]
            country_name = pycountry.countries.get(alpha_2=country_code).name
            weather_request_result = weather_request_result.replace(country_code, f' {country_name}')
        logger.debug(f'Weather request results: {weather_request_result}')
        
        return weather_request_result
    except Exception as e:
        logger.error(f'Exception: {e}')
        return f'Unexpected error: {e}'

