import requests

headers = {
        "accept": "application/json",
        "API-Key": "e46c99ca-f8d7-4ba7-aaf2-99980cb95ab8"
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

def get_bird_details():

    bird_ids = get_bird_ids()

    base_url = "https://nuthatch.lastelm.software/birds/"

    birds_pictures = []

    for bird_id in bird_ids:
        response = requests.get(base_url + str(bird_id), headers=headers)

        data_dictionary = response.json()

        bird_picture = data_dictionary["images"][0]

        birds_pictures.append(bird_picture)

    print("birds_pictures", birds_pictures)

get_bird_details()

        


