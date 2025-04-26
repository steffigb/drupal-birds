import requests
import csv
import os

from dotenv import load_dotenv

load_dotenv()

def get_bird_ids():

    url = "https://nuthatch.lastelm.software/v2/birds?page=1&pageSize=100&region=Western%20Europe&hasImg=true&operator=AND"

    headers = {
        "accept": "application/json",
        "API-Key": os.getenv("API-KEY")
    }

    response = requests.get(url, headers=headers)

    data_dictionary = response.json()
    data_list = data_dictionary["entities"]

    ids = []

    for item in data_list:

        item_id = item["id"]
        ids.append(item_id)

    print("ids", ids)

    with open("bird_data_ids.csv", "w+", newline = "") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(ids)

print(get_bird_ids())