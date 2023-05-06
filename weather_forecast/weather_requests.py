from datetime import datetime, timedelta
from config import OPENWEATHERMAP_API_KEY as API_KEY

import requests
import asyncio
import json

async def __get_emoji(code: int) -> str:
    emoji_map = {
        range(200, 233): '⛈',
        range(300, 322): '🌧',
        range(500, 532): '🌦',
        range(600, 623): '❄️',
        range(701, 782): '🌫',
        800: '☀️',
        801: '🌤',
        802: '⛅️',
        803: '🌥',
        804: '☁️'
    }

    for key, value in emoji_map.items():
        if isinstance(key, int):
            if code == key:
                return value
        elif code in key:
            return value

    return ''

async def __date_to_string(date_str: str) -> str:
    date_object = datetime.strptime(date_str, '%Y-%m-%d')

    day = date_object.day
    suffix = 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')
    formatted_date = date_object.strftime("the {}{} of %B".format(day, suffix))

    return formatted_date

async def __get_weather_forecast(location, lat, lon, days):
    start_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    end_date = start_date + timedelta(days=days + 1)
    start_unix = int(start_date.timestamp())
    end_unix = int(end_date.timestamp())

    url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={lon}&exclude=current,minutely," \
          f"hourly&start={start_unix}&end={end_unix}&appid={API_KEY}"
    response = requests.get(url).json()

    daily_weather = response['daily']

    date_str = await __date_to_string(datetime.fromtimestamp(daily_weather[days]['dt']).strftime("%Y-%m-%d"))
    weather_description = daily_weather[days]['weather'][0]['description']
    temperature_min = daily_weather[days]['temp']['min'] - 273.15
    temperature_max = daily_weather[days]['temp']['max'] - 273.15

    emoji = await __get_emoji(daily_weather[days]['weather'][0]['id'])
    return f"{emoji} On {date_str}, the weather in {location} is expected to be {weather_description} with a minimum " \
           f"temperature of {temperature_min:.2f}°C and a maximum temperature of {temperature_max:.2f}°C."

async def generate_weather_forecast(location, date):
    url = f"http://api.openweathermap.org/geo/1.0/direct?q={location}&limit=1&appid={API_KEY}"
    response = requests.get(url).json()

    lat, lon = response[0]['lat'], response[0]['lon']

    current_date = datetime.now().date()
    date_obj = datetime.strptime(date, '%Y-%m-%d').date()

    diff_days = (date_obj - current_date).days

    if 0 <= diff_days <= 7:
        return await __get_weather_forecast(location, lat, lon, diff_days)
    else:
        return 'wrong_date_message'

async def main():
    my_location, my_date = 'Helsinki', '2023-04-21'
    print(await generate_weather_forecast(my_location, my_date))

if __name__ == '__main__':
    asyncio.run(main())
