import requests


def get_quote() -> str:
    response = requests.get("https://zenquotes.io/api/random").json()
    quote = f'```{response[0]["q"]} -{response[0]["a"]}```'
    return quote
