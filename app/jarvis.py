import discord
import os
import random
import time

from dotenv import load_dotenv

from utils.zip_checker import zip_checker
from utils.city_checker import city_checker

from api.quotes import get_quote
from api.weather import get_weather_zip, get_weather_city

load_dotenv()
client = discord.Client()


########################## start future implementations ##########################
# if using in cli: might need to use sysargv[1] sysargv[2] etc to check user input for certain commands?
# otherwise should work as normal commands in discord

# Planned features:
# -Permanent uptime for discord bot
# -Implement reddit api
# -Implement Twitter api
# -Implement Google calendar api
# -Spotify api
# -flight/travel api
# -nba api
# -hotel bookings
# -airbnb api
# -news
# -urbandictionary
# -recipes
# -words api
# -youtube api


# TBD Features (need to look more into it):
# LinkedIn api
# No database for bot for now, if I ever need one lets implement dynamodb

########################## end future implementations ##########################

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


jarvis_wake_commands = [
    "hello jarvis",
    "hi jarvis",
    "greetings jarvis",
    "jarvis you there",
    "hey jarvis",
    "jarvis hi",
    "jarvis hey",
    "you there jarvis",
    "jarvis hello",
    "jarvis greetings",
]


jarvis_wake_responses = [
    "Hi sir.",
    "At your service, sir.",
    "Hello, sir. Congratulations on the progress so far.",
]

from datetime import datetime

now = datetime.now()
current_time_12 = now.strftime("%m/%d/%Y %I:%M:%S %p")


@client.event
async def on_ready():
    weather_details = get_weather_city("Northridge")
    greeting_weather = weather_details[3:-3]

    print(
        f"Hello sir. Here are your updates for the day: \n\nIt's {current_time_12}.\n\n{greeting_weather}."
    )


@client.event
async def on_message(message: str) -> str:
    get_msg = message.content
    get_jarvis_command = get_msg.split()
    msg = get_msg.lower()

    if message.author == client.user:
        return

    if msg.startswith("!inspire"):
        quote = get_quote()
        await message.channel.send(f"Retrieving random motivational quote...")
        time.sleep(2)
        await message.channel.send(quote)

    if msg.startswith("jarvis weather"):
        # if input was a zip code:
        if zip_checker(get_jarvis_command[2]):
            try:
                if get_jarvis_command[2]:
                    zip_code = get_jarvis_command[2]
                    weather_details = get_weather_zip(zip_code)
                    await message.channel.send(
                        f"Getting weather details for {zip_code}..."
                    )
                    time.sleep(2)
                    await message.channel.send(weather_details)
                else:
                    await message.channel.send("Zip code valid.")
            except:
                await message.channel.send(
                    "No zip code found. Here's the correct format: jarvis weather <zipcode>"
                )
        # elif input was a city input
        elif city_checker(get_jarvis_command[2]):
            try:
                if get_jarvis_command[2] and city_checker(get_jarvis_command[2]):
                    if len(get_jarvis_command) == 3:
                        city_name = {get_jarvis_command[2]}
                        retrieve_msg = f"Getting weather details for {get_jarvis_command[2].capitalize()}..."
                    elif len(get_jarvis_command) == 4:
                        city_name = f"{get_jarvis_command[2]}-{get_jarvis_command[3]}"
                        retrieve_msg = f"Getting weather details for {get_jarvis_command[2].capitalize()} {get_jarvis_command[3].capitalize()}..."
                    elif len(get_jarvis_command) == 5:
                        city_name = f"{get_jarvis_command[2]}-{get_jarvis_command[3]}-{get_jarvis_command[4]}"
                        retrieve_msg = f"Getting weather details for {get_jarvis_command[2].capitalize()} {get_jarvis_command[3].capitalize()} {get_jarvis_command[4].capitalize()}..."
                    weather_details = get_weather_city(city_name)
                    await message.channel.send(retrieve_msg)
                    time.sleep(2)
                    await message.channel.send(weather_details)
                else:
                    await message.channel.send("City name valid.")
            except:
                await message.channel.send(
                    "No city name found. Here's the correct format: jarvis weather <city name>"
                )
        # else, print invalid input
        else:
            await message.channel.send(
                "```Weather request invalid. Did you mean one of these commands?:\njarvis weather <zipcode>\njarvis weather <city>```"
            )

    if any(wake_command in msg.lower() for wake_command in jarvis_wake_commands):
        await message.channel.send(random.choice(jarvis_wake_responses))


client.run(os.getenv("TOKEN"))
client.run(os.getenv("WEATHER_API_KEY"))
