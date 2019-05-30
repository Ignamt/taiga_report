""" Downloads the reports from the taiga api and saves to a file
"""
import requests

report = requests.get(
    "https://taiga.leafnoise.io/api/v1/userstories/csv?"
    "uuid=8687afcceba24795b5b5d77cddf76a0b")

with open("report_csvs\\userstories.csv", "w") as us_csv:
    us_csv.write(report.text)
