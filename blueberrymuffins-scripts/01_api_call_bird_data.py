import requests
import os

from dotenv import load_dotenv

load_dotenv()

def get_bird_data():

    url = "https://nuthatch.lastelm.software/v2/birds?page=1&pageSize=100&region=Western%20Europe&hasImg=true&operator=AND"

    headers = {
        "accept": "application/json",
        "API-Key": os.getenv("API-KEY")
    }

    response = requests.get(url, headers=headers)

    return response.json()

print(get_bird_data())