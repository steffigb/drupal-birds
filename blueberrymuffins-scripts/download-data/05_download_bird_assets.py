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


def download_images(bird_id, image_url):
    
    filename = '../data/' + str(bird_id) + '/' + str(bird_id) + '.jpeg'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    response = requests.get(image_url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)

        file.close()


def download_recordings(bird_id, recording_url):
    
    filename = '../data/' + str(bird_id) + '/' + str(bird_id) + '.mp3'
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    response = requests.get(recording_url)
    if response.status_code == 200:
        with open(filename, 'wb') as file:
            file.write(response.content)

        file.close()


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

        if len(bird_detail["images"]) > 0:
            download_images(bird_detail["id"], bird_detail["images"][0])
        
        if len(bird_detail["recordings"]) > 0:
            download_recordings(bird_detail["id"], bird_detail["recordings"][0]["file"])

    csv_obj.close()


bird_ids = get_bird_ids()
birds_details = get_bird_details(bird_ids)
save_birds_details(birds_details)
