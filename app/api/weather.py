import os
import requests
import datetime as dt
import time


def convert_unix_to_date(unix_string: str) -> str:
    return dt.datetime.fromtimestamp(int(f"{unix_string}")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def convert_kelvin_to_f(kelvin: str) -> int:
    return int(kelvin * 1.8 - 459.67)


def format_time(converted_time: str) -> str:
    converted_split = converted_time.split()
    converted_sunrise_time = converted_split[1]
    time_split = converted_sunrise_time.split(":")
    hour = time_split[0]
    minute = time_split[1]
    hour_min_time = f"{hour}:{minute}"

    preformatted_time = time.strptime(hour_min_time, "%H:%M")
    time_formatted = time.strftime("%I:%M %p", preformatted_time)
    return time_formatted


def get_initial_data_from_zip(zip_code: str) -> dict[str:str]:
    weather_api_key = os.environ["WEATHER_API_KEY"]

    output = {
        "zip": "",
        "city_name": "",
        "country": "",
        "lat": "",
        "lon": "",
    }

    if zip_code:
        try:
            get_initial_info = requests.get(
                f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={weather_api_key}"
            ).json()

            output["zip"] = get_initial_info["zip"]
            output["city_name"] = get_initial_info["name"]
            output["country"] = get_initial_info["country"]
            output["lat"] = get_initial_info["lat"]
            output["lon"] = get_initial_info["lon"]

            return output

        except:
            print(
                f"Error getting weather from http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={weather_api_key}"
            )


def get_initial_data_from_city(city_name_input: str) -> dict[str:str]:
    weather_api_key = os.environ["WEATHER_API_KEY"]

    output = {
        "state": "",
        "city_name": "",
        "country": "",
        "lat": "",
        "lon": "",
    }

    if city_name_input:
        try:
            get_initial_info = requests.get(
                f"http://api.openweathermap.org/geo/1.0/direct?q={city_name_input}&appid={weather_api_key}"
            ).json()

            output["state"] = get_initial_info[0]["state"]
            output["city_name"] = get_initial_info[0]["name"]
            output["country"] = get_initial_info[0]["country"]
            output["lat"] = get_initial_info[0]["lat"]
            output["lon"] = get_initial_info[0]["lon"]

            return output

        except:
            print(
                f"Error getting weather from http://api.openweathermap.org/geo/1.0/direct?q={city_name_input}&appid={weather_api_key}"
            )


def get_weather_zip(zip_code: str) -> str:
    weather_api_key = os.environ["WEATHER_API_KEY"]

    if zip_code:
        try:
            get_initial_info = get_initial_data_from_zip(zip_code)

            city_name = get_initial_info["city_name"]
            country = get_initial_info["country"]
            lat = get_initial_info["lat"]
            lon = get_initial_info["lon"]

            if get_initial_info:
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
                ).json()

                weather_type = response["weather"][0]["main"]

                weather_desc = response["weather"][0]["description"]

                kelvin_temp = response["main"]["temp"]
                fahrenheit = convert_kelvin_to_f(kelvin_temp)

                humidity = response["main"]["humidity"]

                # convert sunrise unix time to local time, show only hour and minute and in 12 hour time + automatically show am/pm
                sunrise = response["sys"]["sunrise"]
                converted_sunrise = convert_unix_to_date(sunrise)
                sunrise_time = format_time(converted_sunrise)

                # convert sunset unix time to local time, show only hour and minute and in 12 hour time + automatically show am/pm
                sunset = response["sys"]["sunset"]
                converted_sunset = convert_unix_to_date(sunset)
                sunset_time = format_time(converted_sunset)

            output_msg = f"```The current weather in {city_name}, {country} is {fahrenheit} degrees with a {weather_desc} and {humidity}% humidity. Forecasts are showing {weather_type} throughout the day.\nSunset for {city_name} will be at {sunset_time} pacific time, and sunrise at {sunrise_time}.```"

        except:
            print(
                f"Error getting weather from http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={weather_api_key}"
            )

    return output_msg


def get_weather_city(city_name_input: str) -> str:
    weather_api_key = os.environ["WEATHER_API_KEY"]

    if city_name_input:
        try:
            get_initial_info = get_initial_data_from_city(city_name_input)

            state = get_initial_info["state"]
            city_name = get_initial_info["city_name"]
            country = get_initial_info["country"]
            lat = get_initial_info["lat"]
            lon = get_initial_info["lon"]

            if get_initial_info:
                response = requests.get(
                    f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={weather_api_key}"
                ).json()

                weather_type = response["weather"][0]["main"]

                weather_desc = response["weather"][0]["description"]

                kelvin_temp = response["main"]["temp"]
                fahrenheit = convert_kelvin_to_f(kelvin_temp)

                humidity = response["main"]["humidity"]

                # convert sunrise unix time to local time, show only hour and minute and in 12 hour time + automatically show am/pm
                sunrise = response["sys"]["sunrise"]
                converted_sunrise = convert_unix_to_date(sunrise)
                sunrise_time = format_time(converted_sunrise)

                # convert sunset unix time to local time, show only hour and minute and in 12 hour time + automatically show am/pm
                sunset = response["sys"]["sunset"]
                converted_sunset = convert_unix_to_date(sunset)
                sunset_time = format_time(converted_sunset)

            output_msg = f"```The current weather in {city_name}, {state} ({country}) is {fahrenheit} degrees with a {weather_desc} and {humidity}% humidity. Forecasts are showing {weather_type} throughout the day.\nSunset for {city_name} will be at {sunset_time} pacific time, and sunrise at {sunrise_time}.```"

        except:
            print(
                f"Error getting weather from http://api.openweathermap.org/geo/1.0/direct?q={city_name_input}&appid={weather_api_key}"
            )

    return output_msg
