import csv

csv_file_path = "../data/birds_details.csv"

with open(csv_file_path, mode ="r") as file:
  csv_file = csv.DictReader(file)
  for bird_detail in csv_file:
        print(f"file; filename=\"{bird_detail['id']}.jpeg\"")
