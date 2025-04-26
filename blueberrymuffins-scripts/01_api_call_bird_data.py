import requests

def get_bird_data():

    url = "https://nuthatch.lastelm.software/v2/birds?page=1&pageSize=100&region=Western%20Europe&hasImg=true&operator=AND"

    headers = {
        "accept": "application/json",
        "API-Key": "e46c99ca-f8d7-4ba7-aaf2-99980cb95ab8"
    }

    response = requests.get(url, headers=headers)

    return response.json()

print(get_bird_data())