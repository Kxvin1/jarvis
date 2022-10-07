from requests import get
from json import dumps


def track_user(ip: str) -> dict[str:str]:
    try:
        response = get(f"https://geolocation-db.com/json/{ip}").json()
    except:
        raise Exception(
            f'Error 500: Data for "{ip}" not able to be retrieved at https://geolocation-db.com/json/{ip} \nIP address not found in the database.'
        )

    formatted_response = dumps(response, indent=4)
    print(f"Jarvis geolocation successful. User Details: \n {formatted_response}")

    return response
