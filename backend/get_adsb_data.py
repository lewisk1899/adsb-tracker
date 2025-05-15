""" Pulls Data From OpenSky """
import json
import os
import time
from datetime import datetime, timezone
from typing import Optional

import requests
from models.state import States

OUTPUT_DIRECTORY = "/data/opensky/"


def poll_open_sky(
    url: str = "https://opensky-network.org/", endpoint: str = "api/states/all"
) -> Optional[States]:
    """ Grabs data from OpenSky Live API """
    try:
        response = requests.get(url + endpoint, timeout=5)
    except requests.exceptions.HTTPError as errh:
        print("Http Error:", errh)
    except requests.exceptions.ConnectionError as errc:
        print("Error Connecting:", errc)
    except requests.exceptions.Timeout as errt:
        print("Timeout Error:", errt)

    if response.status_code == 200:
        data = response.json()
        states = States(**data)
        return states

    return None


def states_to_file(states: States, output_path: str):
    """ Write States to file nambed by the time it was pulled """
    utc_string = states.time
    zulu_time = datetime.fromtimestamp(utc_string, tz=timezone.utc).strftime(
        "%Y-%m-%d %H:%M:%S Z"
    )

    fileout_path = output_path + str(zulu_time) + ".json"

    with open(fileout_path, "w", encoding="utf-8") as fout:
        json.dump(states.model_dump(), fout, indent=4)


def main():
    """ Testing if this works """
    if not os.path.exists(OUTPUT_DIRECTORY):
        os.mkdir(OUTPUT_DIRECTORY)

    while True:
        states = poll_open_sky()
        states_to_file(states, OUTPUT_DIRECTORY)
        time.sleep(600)


if __name__ == "__main__":
    main()
