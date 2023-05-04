from datetime import datetime, timedelta
from config import OPENWEATHERMAP_API_KEY as API_KEY
import requests

def __date_to_string(date_str: str) -> str:
    date_object = datetime.strptime(date_str, '%Y-%m-%d')

    day = date_object.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    formatted_date = date_object.strftime("the {}{} of %B".format(day, suffix))

    return formatted_date


def __get_weather_forecast(location, lat, lon, days):
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=days + 1)
    start_unix = int(start_date.timestamp())
    end_unix = int(end_date.timestamp())

    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely," \
          f"hourly&start={start_unix}&end={end_unix}&appid={API_KEY}"
    response = requests.get(url).json()

    daily_weather = response['daily']

    date_str = __date_to_string(datetime.fromtimestamp(daily_weather[days]['dt']).strftime("%Y-%m-%d"))
    weather_description = daily_weather[days]['weather'][0]['description']
    temperature_min = daily_weather[days]['temp']['min'] - 273.15
    temperature_max = daily_weather[days]['temp']['max'] - 273.15
    return f"On {date_str}, the weather in {location} is expected to be {weather_description} with a minimum " \
           f"temperature of {temperature_min:.2f}°C and a maximum temperature of {temperature_max:.2f}°C."

def __get_weather_today(location, lat, lon, date):
    date_unix = int(datetime.strptime(date, "%Y-%m-%d").timestamp())

    url = f"https://api.openweathermap.org/data/2.5/onecall/timemachine?lat={lat}&lon={lon}" \
          f"&dt={date_unix}&appid={API_KEY}"
    response = requests.get(url).json()

    weather_description = response['current']['weather'][0]['description']
    temperature = response['current']['temp'] - 273.15

    return f"The weather in {location} on {__date_to_string(date)} is {weather_description} with " \
           f"a temperature of {temperature:.2f}°C."

def generate_weather_forecast(location, date):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
    response = requests.get(url).json()

    lat, lon = response[0]['lat'], response[0]['lon']

    current_date = datetime.now().date()
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    diff_days = (date_obj - current_date).days

    if diff_days == 0:
        return __get_weather_today(location, lat, lon, date)
    elif 0 < diff_days < 8:
        return __get_weather_forecast(location, lat, lon, diff_days)
    else:
        return 'Wrong date specified'

if __name__ == '__main__':
    my_location, my_date = 'Helsinki', '2023-04-21'
    print(generate_weather_forecast(my_location, my_date))
