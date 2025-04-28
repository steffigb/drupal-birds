import requests
import csv
import os

from dotenv import load_dotenv

load_dotenv()

headers = {
        "accept": "application/json",
        "API-Key": os.getenv("API-KEY")
    }

def get_bird_ids():

    url = "https://nuthatch.lastelm.software/v2/birds?page=1&pageSize=100&region=Western%20Europe&hasImg=true&operator=AND"

    response = requests.get(url, headers=headers)

    data_dictionary = response.json()
    data_list = data_dictionary["entities"]

    ids = []

    for item in data_list:
        
        item_id = item["id"]
        ids.append(item_id)
    
    return ids

def get_bird_details(bird_ids):

    base_url = "https://nuthatch.lastelm.software/birds/"

    birds_details = []

    for bird_id in bird_ids:
        response = requests.get(base_url + str(bird_id), headers=headers)

        data_dictionary = response.json()
        birds_details.append(data_dictionary)

    return birds_details

def save_birds_details(birds_details):

    birds_details_header = ["images", "name", "id", "sciName", "region", "status", "recordings"]

    csv_file = '../data/birds_details.csv'
    csv_obj = open(csv_file, 'w')

    csv_writer = csv.writer(csv_obj)
    header = birds_details_header
    csv_writer.writerow(header)

    for bird_detail in birds_details:
        filtered_bird_detail= {}

        for header in birds_details_header:
            if header in bird_detail:
                filtered_bird_detail[header] = bird_detail[header]
        csv_writer.writerow(filtered_bird_detail.values())

    csv_obj.close()


bird_ids = get_bird_ids()
birds_details = get_bird_details(bird_ids)
save_birds_details(birds_details)
