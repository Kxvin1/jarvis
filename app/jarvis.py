import discord
import os
import requests
import random

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
    "jarvis weather",  # grab weather from api
    "jarvis time"  # grab time
    "jarvis forecast"  # grab forecast from api
    "jarvis create to do",  # create a formatted message block
    "jarvis locate",  # locate user via ip (geolocate api)
    "jarvis add url",  # post url
    "jarvis set alarm",  # ping me at set time (discord webhook?)
    "jarvis send email",  # send email from my email address (google key, refer to my amz scraper project)
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
]
########################## end future implementations ##########################


sad_words = ["sad", "sadge", "unhappy"]


starter_encouragements = [
    "dont be sadge",
    "hang in there",
    "cheer up",
]


def get_quote() -> str:
    response = requests.get("https://zenquotes.io/api/random").json()
    quote = f'{response[0]["q"]} -{response[0]["a"]}'
    print(type(quote))
    return quote


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

    if message.author == client.user:
        return

    if msg.startswith("$hello"):
        await message.channel.send("Oh, hello sir.")

    if msg.startswith("$inspire"):
        quote = get_quote()
        await message.channel.send(quote)

    if any(word in msg for word in sad_words):
        await message.channel.send(random.choice(starter_encouragements))

    print(type(msg), "msg type")


client.run(os.getenv("TOKEN"))
