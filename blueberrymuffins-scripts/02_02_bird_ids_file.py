import requests
import csv

def get_bird_ids():

    url = "https://nuthatch.lastelm.software/v2/birds?page=1&pageSize=100&region=Western%20Europe&hasImg=true&operator=AND"

    headers = {
        "accept": "application/json",
        "API-Key": "e46c99ca-f8d7-4ba7-aaf2-99980cb95ab8"
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