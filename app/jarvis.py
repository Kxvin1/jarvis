import discord
import os
import random
import time

from dotenv import load_dotenv

from utils import zip_checker, city_checker, get_current_time
from api import quotes, weather, google_calendar, geolocate

load_dotenv()
client = discord.Client()

jarvis_commands = [
    "j commands --> list all available commands"
    "j inspire me --> grab random quote from quotes api",
    "j weather --> grab weather from api (via zipcode or city name)",
    "j track --> geolocate a user by ip address",
    "j create calendar event --> create google calendar event",
]


jarvis_wake_commands = [
    "hello jarvis",
    "jarvis hello",
    "hi jarvis",
    "jarvis hi",
    "greetings jarvis",
    "jarvis greetings",
    "you there jarvis",
    "jarvis you there",
    "hey jarvis",
    "jarvis hey",
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


# JARVIS -- RUNS ONCE ON BOOTUP, PRINTS TO TERMINAL
@client.event
async def on_ready():
    current_time = get_current_time.get_current_time()

    weather_details = weather.get_weather_city("Northridge")
    greeting_weather = weather_details[3:-3]

    print(
        f"Hello sir. Here are your updates for the day: \n\nIt's {current_time}.\n\n{greeting_weather}"
    )


# ---------------------------------------------

# -------
# JARVIS COMMANDS
# -------

# JARVIS -- EVENT LISTENERS - SENDS MESSAGES TO DISCORD SERVER BASED ON COMMAND
@client.event
async def on_message(message: str) -> str:
    get_msg = message.content
    get_jarvis_command = get_msg.split()
    msg = get_msg.lower()  # make commands case insensitive

    # IGNORE COMMANDS FROM SELF (JARVIS BOT)
    if message.author == client.user:
        return

    # JARVIS -- LIST COMMANDS
    if msg.startswith("j commands"):
        await message.channel.send("Here are my available commands:")
        commands_as_str = "\n".join(jarvis_commands)
        await message.channel.send(f"```{commands_as_str}```")

    # JARVIS -- WEATHER FORECAST AND TIME UPDATE (GIVES TIME AND WEATHER FOR ADMIN USER)
    if msg.startswith("j update"):
        jarvis_update_current_time = get_current_time.get_current_time()

        weather_details = weather.get_weather_city("Northridge")
        greeting_weather = weather_details[3:-3]
        output = f"```Hello sir, here's are your updates: \n\nIt's {jarvis_update_current_time}.\n\n{greeting_weather}```"
        await message.channel.send(output)

    # JARVIS -- JARVIS GREETING
    if any(wake_command in msg.lower() for wake_command in jarvis_wake_commands):
        await message.channel.send(random.choice(jarvis_wake_responses))

    # JARVIS -- TRACK USER
    if msg.startswith("j track"):
        if get_jarvis_command[2]:
            try:
                ip = get_jarvis_command[2]
                user_details = geolocate.track_user(ip)

                user_country = user_details["country_name"]
                user_state = user_details["state"]
                user_city = user_details["city"]
                user_postal = user_details["postal"]
                user_latitude = user_details["latitude"]
                user_longitude = user_details["longitude"]

                google_map_url = (
                    f"https://www.google.com/maps?q={user_latitude},{user_longitude}"
                )

                await message.channel.send(f"Locating user with IP address {ip} ...")
                time.sleep(1)

                track_msg = (
                    f"```"
                    f"Details for IP address {ip} found. Here are the user's details:\n\n"
                    f"Country: {user_country}\n"
                    f"State: {user_state}\n"
                    f"City: {user_city}\n"
                    f"Zip code: {user_postal}\n"
                    f"Latitude,Longitude: {user_latitude},{user_longitude}"
                    f"```"
                )

                await message.channel.send(track_msg)
                await message.channel.send(
                    f"Google Map to user's location:\n<{google_map_url}>"
                )
            except:
                await message.channel.send(
                    f"Error 500: Data for '{ip}' not able to be retrieved at https://geolocation-db.com/json/{ip} \nIP address not found in the database."
                )

    # JARVIS -- INSPIRATIONAL QUOTES API FETCHING
    if msg.startswith("j inspire me"):
        quote = quotes.get_quote()
        await message.channel.send(f"Retrieving random motivational quote...")
        time.sleep(1)
        await message.channel.send(quote)

    # JARVIS -- WEATHER API FETCHING
    if msg.startswith("j weather"):
        # if input was a zip code:
        if zip_checker.zip_checker(get_jarvis_command[2]):
            try:
                if get_jarvis_command[2]:
                    zip_code = get_jarvis_command[2]
                    weather_details = weather.get_weather_zip(zip_code)
                    await message.channel.send(
                        f"Getting weather details for {zip_code}..."
                    )
                    time.sleep(1)
                    await message.channel.send(weather_details)
                else:
                    await message.channel.send("Zip code invalid.")
            except:
                await message.channel.send(
                    f"Zip code {zip_code} not found. Here's the correct format: j weather <zipcode>"
                )
        # elif input was a city input
        elif city_checker.city_checker(get_jarvis_command[2]):
            try:
                if get_jarvis_command[2] and city_checker.city_checker(
                    get_jarvis_command[2]
                ):
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

                    weather_details = weather.get_weather_city(city_name)
                    await message.channel.send(retrieve_msg)
                    time.sleep(1)
                    await message.channel.send(weather_details)
                else:
                    await message.channel.send("City name invalid.")
            except:
                await message.channel.send(
                    f"City name '{city_name}' not found. Here's the correct format: j weather <city name>"
                )
        # else, print invalid input
        else:
            invalid_weather_command_output = " ".join(get_jarvis_command[2:])

            weather_except_msg = (
                f"```"
                f"Weather request for input '{invalid_weather_command_output}' is invalid."
                f" Make sure to put a valid zip code (i.e. 90210) or city name (i.e. Seattle).\n\n"
                f"Did you mean one of these commands?:\n"
                f"j weather <zipcode>\n"
                f"j weather <city>"
                f"```"
            )

            await message.channel.send(weather_except_msg)

    # JARVIS -- CREATE GOOGLE CALENDAR EVENT
    if msg.startswith("j create calendar event"):
        if len(get_jarvis_command) >= 4:
            try:
                calendar_event_details = " ".join(get_jarvis_command[4:])
                calendar_event_details_inputs = calendar_event_details.split("/")

                # expected input to create a calendar event
                # St_Month/St_Day/St_Year/St_Hour/St_Min/End_Month/End_Day/End_Year/End_Hour/End_Min/Title/Desc/Location (13 inputs)

                start_month_input = int(calendar_event_details_inputs[0])
                start_day_input = int(calendar_event_details_inputs[1])
                start_year_input = int(calendar_event_details_inputs[2])
                start_hour_input = int(calendar_event_details_inputs[3])
                start_minute_input = int(calendar_event_details_inputs[4])
                end_month_input = int(calendar_event_details_inputs[5])
                end_day_input = int(calendar_event_details_inputs[6])
                end_year_input = int(calendar_event_details_inputs[7])
                end_hour_input = int(calendar_event_details_inputs[8])
                end_minute_input = int(calendar_event_details_inputs[9])
                event_title_input = calendar_event_details_inputs[10]
                description_input = calendar_event_details_inputs[11]
                # location requires very last input to be the location for this to work properly
                location_input = "/".join(calendar_event_details_inputs[12:])

                await message.channel.send(f"Creating new Google Calendar event...")
                google_calendar.create_google_calendar_event(
                    start_month_input,
                    start_day_input,
                    start_year_input,
                    start_hour_input,
                    start_minute_input,
                    end_month_input,
                    end_day_input,
                    end_year_input,
                    end_hour_input,
                    end_minute_input,
                    event_title_input,
                    description_input,
                    location_input,
                )
                time.sleep(1)

                start_postfix = "am"
                if start_hour_input > 12:
                    start_postfix = "pm"
                    start_hour_input -= 12

                end_postfix = "am"
                if end_hour_input > 12:
                    end_postfix = "pm"
                    end_hour_input -= 12

                start_extra_zero = ""
                if start_minute_input <= 9:
                    start_extra_zero = 0

                end_extra_zero = ""
                if end_minute_input <= 9:
                    end_extra_zero = 0

                start_user_info_print = f"{start_hour_input}:{start_extra_zero}{start_minute_input}{start_postfix}"
                end_user_info_print = (
                    f"{end_hour_input}:{end_extra_zero}{end_minute_input}{end_postfix}"
                )

                calendar_created_msg = (
                    f"Event created! Here are the details.\n"
                    f"```"
                    f"Start Date: {start_month_input}-{start_day_input}-{start_year_input} at {start_user_info_print}\n"
                    f"End Date: {end_month_input}-{end_day_input}-{end_year_input} at {end_user_info_print}\n"
                    f"Event Title: {event_title_input}\n"
                    f"Description: {description_input}\n"
                    f"Location: {location_input}"
                    f"```"
                )

                await message.channel.send(calendar_created_msg)

            except:
                invalid_calendar_command_output = " ".join(get_jarvis_command[4:])

                calendar_except_msg = (
                    f"```"
                    f"Calendar creation request for input '{invalid_calendar_command_output}' is invalid. Make sure to input all 13 required inputs in the following order.\n\n"
                    f"Here are the 13 inputs and the required order:\n"
                    f"Start Month\n"
                    f"Start Day\n"
                    f"Start Year\n"
                    f"Start Hour\n"
                    f"Start Minute\n"
                    f"End Month\n"
                    f"End Day\n"
                    f"End Year\n"
                    f"End Hour\n"
                    f"End Minute\n"
                    f"Event Title\n"
                    f"Description\n"
                    f"Location\n\n"
                    f"Here's the correct format of this command:\n"
                    f"j create calendar event start_year/start_month/start_day/start_hour/start_minute/end_year/end_month/end_day/end_hour/end_minute/event_title/event_description/event_location\n\nExample:\nj create calendar event 12/25/2023/14/00/12/25/2023/17/00/Final Interview at Tech Company/Final round to join Team JARVIS/www.zoom.com/initiative"
                    f"```"
                )

                await message.channel.send(calendar_except_msg)


# ---------------------------------------------

client.run(os.getenv("TOKEN"))
client.run(os.getenv("WEATHER_API_KEY"))
