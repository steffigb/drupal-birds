import ast
import csv
import json
import requests

csv_file_path = "../data/birds_details.csv"

with open(csv_file_path, mode="r") as file:
    csv_file = csv.DictReader(file)
    for bird_detail in csv_file:
        print(bird_detail)

        # Upload photo and use its uuid from response for bird entry creation later
        with open(
            f"../data/{bird_detail['id']}/{bird_detail['id']}.jpeg", "rb"
        ) as photo:
            photo_data_payload = photo.read()

        photo_upload_url = (
            "https://blueberrymuffins.ddev.site/jsonapi/node/bird/field_photo"
        )

        photo_request_headers = {
            "Content-Type": "application/octet-stream",
            "Accept": "application/vnd.api+json",
            "Content-Disposition": f"file; filename=\"{bird_detail['id']}.jpeg\"",
        }

        photo_upload_response = requests.request(
            "POST",
            photo_upload_url,
            headers=photo_request_headers,
            data=photo_data_payload,
        )

        if photo_upload_response.status_code == 201:
            print(f"Photo uploaded: {bird_detail['id']}")
            photo_uuid = photo_upload_response.json()["data"]["id"]
        else:
            raise Exception(f"Photo upload failed: {photo_upload_response.text}")

        # Upload recording and use its uuid from response for bird entry creation later

        recordings = bird_detail.get("recordings", "").strip()
        if recordings and recordings != "[]":
            with open(
                f"../data/{bird_detail['id']}/{bird_detail['id']}.mp3", "rb"
            ) as recording:
                recording_data_payload = recording.read()

            recording_upload_url = (
                "https://blueberrymuffins.ddev.site/jsonapi/node/bird/field_recording"
            )

            recording_request_headers = {
                "Content-Type": "application/octet-stream",
                "Accept": "application/vnd.api+json",
                "Content-Disposition": f"file; filename=\"{bird_detail['id']}.mp3\"",
            }

            recording_upload_response = requests.request(
                "POST",
                recording_upload_url,
                headers=recording_request_headers,
                data=recording_data_payload,
            )

            if recording_upload_response.status_code == 201:
                print(f"Recording uploaded: {bird_detail['id']}")
                recording_uuid = recording_upload_response.json()["data"]["id"]
            else:
                raise Exception(
                    f"Recording upload failed: {recording_upload_response.text}"
                )

        # Upload bird data for bird entry creation
        bird_entry_url = "https://blueberrymuffins.ddev.site/jsonapi/node/bird/"

        bird_entry = {
            "data": {
                "type": "node--bird",
                "attributes": {
                    "title": bird_detail["name"],
                    "field_id": bird_detail["id"],
                    "field_location": ast.literal_eval(bird_detail["region"]),
                    "field_scientific_name": bird_detail["sciName"],
                    "field_status": bird_detail["status"]
                    .lower()
                    .replace(" ", "_")
                },
                "relationships": {
                    "field_photo": {"data": {"type": "file--file", "id": photo_uuid}}
                },
            }
        }

        if recordings and recordings != "[]":
            recording_entry = {"data": {"type": "file--file", "id": recording_uuid}}
            bird_entry["data"]["relationships"]["field_recording"] = recording_entry

        bird_entry_payload = json.dumps(bird_entry)

        bird_entry_headers = {
            "Content-Type": "application/vnd.api+json",
            "Accept": "application/vnd.api+json",
        }

        bird_entry_response = requests.request(
            "POST", bird_entry_url, headers=bird_entry_headers, data=bird_entry_payload
        )

        if bird_entry_response.status_code == 201:
            print(f"Bird entry created: {bird_detail['id']}")
        else:
            raise Exception(f"Bird entry creation failed: {bird_entry_response.text}")
