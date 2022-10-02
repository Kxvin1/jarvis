import discord
import os
import requests
import random
import datetime as dt
import time

from dotenv import load_dotenv

load_dotenv()
client = discord.Client()


########################## start future implementations ##########################
# if using in cli: might need to use sysargv[1] sysargv[2] etc to check user input for certain commands?
# otherwise should work as normal commands in discord
jarvis_commands = [
    "jarvis wake up",  # start jarvis
    "jarvis power off",  # stop jarvis
    "jarvis stealth",  # sleep jarvis
    "jarvis weather",  # grab weather from api -- IMPLEMENTED. just needs touching up
    "jarvis time"  # grab time
    "jarvis forecast"  # grab forecast from api
    "jarvis create to do",  # create a formatted message block
    "jarvis locate",  # locate user via ip (geolocate api)
    "jarvis add url",  # post url
    "jarvis set alarm",  # ping me at set time (discord webhook?)
    "jarvis send email",  # send email from my email address (google key, refer to my amz scraper project)
    "jarvis track",  # use geolocation db to track user by ip address (geolocate)
]

jarvis_actions = [
    "wakeup [action]",
    "poweroff [action]",
    "stealth [action]",
    "weather [action]",
    "time [action]",
    "forecast [action]",
    "create to do [action]",
    "locate [action]",
    "add url [action]",
    "set alarm [action]",
    "send email [action]",
    "track [action]",
]
########################## end future implementations ##########################


jarvis_wake_commands = [
    "hello jarvis",
    "hi jarvis",
    "greetings jarvis",
    "jarvis you there",
    "hey jarvis",
]


jarvis_wake_responses = [
    "For you sir, always.",
    "At your service, sir.",
    "Hello, sir. Congratulations on the progress so far.",
]


def get_quote() -> str:
    response = requests.get("https://zenquotes.io/api/random").json()
    quote = f'{response[0]["q"]} -{response[0]["a"]}'
    return quote


def convert_unix_to_date(unix_string):
    return dt.datetime.fromtimestamp(int(f"{unix_string}")).strftime(
        "%Y-%m-%d %H:%M:%S"
    )


def get_weather(zip_code: str) -> str:
    weather_api_key = os.environ["WEATHER_API_KEY"]

    if zip_code:

        try:
            get_initial_info = requests.get(
                f"http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={weather_api_key}"
            ).json()

            zip = get_initial_info["zip"]
            city_name = get_initial_info["name"]
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
                temp = int(kelvin_temp * 1.8 - 459.67)

                humidity = response["main"]["humidity"]

                # convert sunrise unix time to local time, show only hour and minute and in 12 hour time + automatically show am/pm
                sunrise = response["sys"]["sunrise"]
                converted_sunrise = convert_unix_to_date(sunrise)
                converted_sunrise_split = converted_sunrise.split()
                converted_sunrise_time = converted_sunrise_split[1]
                sunrise_time_split = converted_sunrise_time.split(":")
                sunrise_hour = sunrise_time_split[0]
                sunrise_minute = sunrise_time_split[1]
                sunrise_time = f"{sunrise_hour}:{sunrise_minute}"

                sunrise_t = time.strptime(sunrise_time, "%H:%M")
                sunrise_timevalue_12hour = time.strftime("%I:%M %p", sunrise_t)

                # convert sunset unix time to local time, show only hour and minute and in 12 hour time + automatically show am/pm
                sunset = response["sys"]["sunset"]
                converted_sunset = convert_unix_to_date(sunset)
                converted_sunset_split = converted_sunset.split()
                converted_sunset_time = converted_sunset_split[1]
                sunset_time_split = converted_sunset_time.split(":")
                sunset_hour = sunset_time_split[0]
                sunset_minute = sunset_time_split[1]
                sunset_time = f"{sunset_hour}:{sunset_minute}"

                sunset_t = time.strptime(sunset_time, "%H:%M")
                sunset_timevalue_12hour = time.strftime("%I:%M %p", sunset_t)

            output_msg = f"The weather in {city_name}, {country} is {temp} degrees with a {weather_desc} and {humidity}% humidity. Forecasts are showing {weather_type} throughout the day.\nSunset will be at {sunset_timevalue_12hour}, with sunrise at {sunrise_timevalue_12hour}."

        except:
            print(
                f"Error getting weather from http://api.openweathermap.org/geo/1.0/zip?zip={zip_code}&appid={weather_api_key}"
            )

    return output_msg


@client.event
async def on_ready():
    # how it should look when weather, time, and forecast are implemented:
    # print(
    #     f"Good morning sir. \nHere are your updates for the day: \nIt's <time>. The weather in <location> is <temperature in degrees> degrees with <short forecast>. <longer forecast>."
    # )

    print(
        f"Good morning sir. Here are your updates for the day: \nIt's 7 A.M. The weather in Malibu is 72 degrees with scattered clouds. The surf conditions are fair with waist to shoulder highlines, high tide will be at 10:52 a.m."
    )


@client.event
async def on_message(message: str) -> str:
    msg = message.content
    get_jarvis_command = msg.split()

    if message.author == client.user:
        return

    if msg.startswith("!inspire"):
        quote = get_quote()
        await message.channel.send(f"Retrieving random motivational quote...")
        time.sleep(2)
        await message.channel.send(quote)

    if msg.startswith("jarvis weather"):
        # get weather via zip code
        if get_jarvis_command[2]:
            try:
                zip_code = get_jarvis_command[2]
                weather_details = get_weather(zip_code)
                await message.channel.send(f"Getting weather details for {zip_code}...")
                time.sleep(2)
                await message.channel.send(weather_details)
            except:
                await message.channel.send("Zip code was not valid.")

    if any(wake_command in msg for wake_command in jarvis_wake_commands):
        await message.channel.send(random.choice(jarvis_wake_responses))


client.run(os.getenv("TOKEN"))
client.run(os.getenv("WEATHER_API_KEY"))
