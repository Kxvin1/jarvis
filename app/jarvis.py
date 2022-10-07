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

from api.google_calendar import create_google_calendar_event

load_dotenv()
client = discord.Client()


jarvis_commands = [
    "jarvis weather",  # grab weather from api -- IMPLEMENTED. just needs touching up/refactoring
    "jarvis track",  # use geolocation db to track user by ip address (geolocate)
    "jarvis create calendar event",  # use google calendar api to create a calendar event
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
        f"Hello sir. Here are your updates for the day: \n\nIt's {current_time}.\n\n{greeting_weather}"
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

    # JARVIS -- WEATHER FORECAST AND TIME UPDATE (GIVES TIME AND WEATHER FOR ADMIN USER)
    if msg.startswith("j update"):
        jarvis_update_current_time = get_current_time()

        weather_details = get_weather_city("Northridge")
        greeting_weather = weather_details[3:-3]
        output = f"```Hello sir, here's are your updates: \n\nIt's {jarvis_update_current_time}.\n\n{greeting_weather}```"
        await message.channel.send(output)

    # JARVIS -- JARVIS GREETING
    if any(wake_command in msg.lower() for wake_command in jarvis_wake_commands):
        await message.channel.send(random.choice(jarvis_wake_responses))

    # JARVIS -- INSPIRATIONAL QUOTES API FETCHING
    if msg.startswith("j inspire me"):
        quote = get_quote()
        await message.channel.send(f"Retrieving random motivational quote...")
        time.sleep(2)
        await message.channel.send(quote)

    # JARVIS -- WEATHER API FETCHING
    if msg.startswith("j weather"):
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
            invalid_weather_command_output = " ".join(get_jarvis_command[2:])
            await message.channel.send(
                f"```Weather request for input '{invalid_weather_command_output}' is invalid. Make sure to put a valid zip code (i.e. 90210) or city name (i.e. Seattle).\n\nDid you mean one of these commands?:\njarvis weather <zipcode>\njarvis weather <city>```"
            )

    # JARVIS -- CREATE GOOGLE CALENDAR EVENT
    if msg.startswith("j create calendar event"):
        if len(get_jarvis_command) >= 4:
            try:
                calendar_event_details = " ".join(get_jarvis_command[4:])
                calendar_event_details_inputs = calendar_event_details.split("/")

                start_year_input = int(calendar_event_details_inputs[0])
                start_month_input = int(calendar_event_details_inputs[1])
                start_day_input = int(calendar_event_details_inputs[2])
                start_hour_input = int(calendar_event_details_inputs[3])
                start_minute_input = int(calendar_event_details_inputs[4])
                end_year_input = int(calendar_event_details_inputs[5])
                end_month_input = int(calendar_event_details_inputs[6])
                end_day_input = int(calendar_event_details_inputs[7])
                end_hour_input = int(calendar_event_details_inputs[8])
                end_minute_input = int(calendar_event_details_inputs[9])
                event_title_input = calendar_event_details_inputs[10]
                description_input = calendar_event_details_inputs[11]
                # location requires very last input to be the location for this to work properly
                location_input = "/".join(calendar_event_details_inputs[12:])

                await message.channel.send(f"Creating new Google Calendar event...")
                create_google_calendar_event(
                    start_year_input,
                    start_month_input,
                    start_day_input,
                    start_hour_input,
                    start_minute_input,
                    end_year_input,
                    end_month_input,
                    end_day_input,
                    end_hour_input,
                    end_minute_input,
                    event_title_input,
                    description_input,
                    location_input,
                )
                time.sleep(2)

                start_postfix = "am"
                if start_hour_input > 12:
                    start_postfix = "pm"
                    start_hour_input -= 12

                end_postfix = "am"
                if end_hour_input > 12:
                    end_postfix = "pm"
                    end_hour_input -= 12

                start_user_info_print = (
                    f"{start_hour_input}:{start_minute_input}{start_postfix}"
                )
                end_user_info_print = (
                    f"{end_hour_input}:{end_minute_input}{end_postfix}"
                )

                await message.channel.send(
                    f"Event created! Here are the details.\n```Start Date: {start_month_input}-{start_day_input}-{start_year_input} at {start_user_info_print}\nEnd Date: {end_month_input}-{end_day_input}-{end_year_input} at {end_user_info_print}\nEvent Title: {event_title_input}\nDescription: {description_input}\nLocation: {location_input}```"
                )

            except:
                invalid_calendar_command_output = " ".join(get_jarvis_command[4:])
                await message.channel.send(
                    f"```Calendar creation request for input '{invalid_calendar_command_output}' is invalid. Make sure to input all 13 required inputs in the following order.\n\nHere are the 13 inputs and the required order:\nstart_year\nstart_month\nstart_day\nstart_hour\nstart_minute\nend_year\nend_month\nend_day\nend_hour\nend_minute\nevent_title\ndescription -- optional, but command must end in a '/'-- ex: title_here/\nlocation -- optional\n\nHere's the correct format of this command:\nj create calendar event start_year/start_month/start_day/start_hour/start_minute/end_year/end_month/end_day/end_hour/end_minute/event_title/event_description/event_location\n\nExample:\nj create calendar event 2022/11/16/18/30/2022/11/16/19/30/meeting with jeff bezos about the price of bananas/very long description info filled with much details/www.amazon.com/bananas```"
                )


client.run(os.getenv("TOKEN"))
client.run(os.getenv("WEATHER_API_KEY"))
