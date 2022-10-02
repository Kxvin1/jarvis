import discord
import os
import random
import time

from dotenv import load_dotenv

from utils.zip_checker import zip_checker
from utils.city_checker import city_checker
from utils.get_current_time import get_current_time

from api.quotes import get_quote
from api.weather import get_weather_zip, get_weather_city

load_dotenv()
client = discord.Client()


########################## start implementations ##########################
# if using in cli: might need to use sysargv[1] sysargv[2] etc to check user input for certain commands?
# otherwise should work as normal commands in discord using msg.startswith

# implemented features:
# 1. inspirational quote api
# 2. jarvis basic greetings (jarvis will reply with preset greetings based on what you say)
# 3. retrieve weather api, using zipcode or city name

# currently working on:
# 1. google calendar api implementation

# Planned features:
# -Implement Google calendar api
# -Permanent uptime for discord bot
# -Implement reddit api
# -Implement Twitter api
# -youtube api
# -Spotify api
# -flight/travel api
# -news
# -hotel bookings
# -nba api
# -airbnb api
# -urbandictionary
# -recipes
# -words api


# TBD Features (need to look more into it):
# LinkedIn api
# No database for bot for now, if I ever need one lets implement dynamodb

########################## end implementations ##########################

jarvis_commands = [
    "jarvis weather",  # grab weather from api -- IMPLEMENTED. just needs touching up/refactoring
    "jarvis time"  # grab time
    "jarvis forecast"  # grab forecast from api
    "jarvis create to do",  # create a formatted message block
    "jarvis locate",  # locate user via ip (geolocate api)
    "jarvis add url",  # post url
    "jarvis set alarm",  # ping me at set time (discord webhook?)
    "jarvis send email",  # send email from my email address (google key, refer to my amz scraper project)
    "jarvis track",  # use geolocation db to track user by ip address (geolocate)
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
    "wake up jarvis",
    "jarvis wake up",
    "wakeup jarvis",
    "jarvis wakeup",
]


jarvis_wake_responses = [
    "Hi sir.",
    "At your service, sir.",
    "Hello, sir. Congratulations on the progress so far.",
]


# JARVIS -- RUNS ONCE ON START, PRINTS TO TERMINAL
@client.event
async def on_ready():
    current_time = get_current_time()

    weather_details = get_weather_city("Northridge")
    greeting_weather = weather_details[3:-3]

    print(
        f"Hello sir. Here are your updates for the day: \n\nIt's {current_time}.\n\n{greeting_weather}."
    )


# JARVIS -- EVENT LISTENERS - SENDS MESSAGES TO DISCORD SERVER BASED ON COMMAND
@client.event
async def on_message(message: str) -> str:
    get_msg = message.content
    get_jarvis_command = get_msg.split()
    msg = get_msg.lower()  # make commands case insensitive

    # IGNORE COMMANDS FROM SELF (JARVIS BOT)
    if message.author == client.user:
        return

    # JARVIS -- SIMPLE UPDATE (GIVES TIME AND WEATHER FOR ADMIN USER)
    if msg.startswith("jarvis update"):
        jarvis_update_current_time = get_current_time()

        weather_details = get_weather_city("Northridge")
        greeting_weather = weather_details[3:-3]
        output = f"```Hello sir, here's are your updates: \n\nIt's {jarvis_update_current_time}.\n\n{greeting_weather}.```"
        await message.channel.send(output)

    # JARVIS -- SIMPLE JARVIS GREETING
    if any(wake_command in msg.lower() for wake_command in jarvis_wake_commands):
        await message.channel.send(random.choice(jarvis_wake_responses))

    # JARVIS -- INSPIRATIONAL QUOTES API FETCHING
    if msg.startswith("!inspire"):
        quote = get_quote()
        await message.channel.send(f"Retrieving random motivational quote...")
        time.sleep(2)
        await message.channel.send(quote)

    # JARVIS -- WEATHER API FETCHING
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
                    await message.channel.send("Zip code invalid.")
            except:
                await message.channel.send(
                    f"Zip code {zip_code} not found. Here's the correct format: jarvis weather <zipcode>"
                )
        # elif input was a city input
        elif city_checker(get_jarvis_command[2]):
            try:
                if get_jarvis_command[2] and city_checker(get_jarvis_command[2]):
                    # city with 1 name
                    if len(get_jarvis_command) == 3:
                        city_name = {get_jarvis_command[2]}
                        retrieve_msg = f"Getting weather details for {get_jarvis_command[2].capitalize()}..."

                    # city with 2 names
                    elif len(get_jarvis_command) == 4:
                        city_name = f"{get_jarvis_command[2]}-{get_jarvis_command[3]}"
                        retrieve_msg = f"Getting weather details for {get_jarvis_command[2].capitalize()} {get_jarvis_command[3].capitalize()}..."

                    # city with 3 names
                    elif len(get_jarvis_command) == 5:
                        city_name = f"{get_jarvis_command[2]}-{get_jarvis_command[3]}-{get_jarvis_command[4]}"
                        retrieve_msg = f"Getting weather details for {get_jarvis_command[2].capitalize()} {get_jarvis_command[3].capitalize()} {get_jarvis_command[4].capitalize()}..."

                    weather_details = get_weather_city(city_name)
                    await message.channel.send(retrieve_msg)
                    time.sleep(2)
                    await message.channel.send(weather_details)
                else:
                    await message.channel.send("City name invalid.")
            except:
                await message.channel.send(
                    f"City name '{city_name}' not found. Here's the correct format: jarvis weather <city name>"
                )
        # else, print invalid input
        else:
            await message.channel.send(
                f"```Weather request for input '{get_jarvis_command[2]}' is invalid. Make sure to put a valid zip code (i.e. 90210) or city name (i.e. Seattle).\n\nDid you mean one of these commands?:\njarvis weather <zipcode>\njarvis weather <city>```"
            )


client.run(os.getenv("TOKEN"))
client.run(os.getenv("WEATHER_API_KEY"))
