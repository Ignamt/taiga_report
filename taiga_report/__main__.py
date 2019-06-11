"""Executes the report generator and updates the reported User Stories."""
import yaml

from .taiga_api import TaigaAPI
from .classes import Report, UserStory

with open("api.yaml", "r") as yaml_file:
    yaml_dict = yaml.load(yaml_file)
api = TaigaAPI("sieel", yaml_dict)
us_list = api.download_user_stories()

report = Report("SIEEL", yaml_dict)

for us_json in us_list:
    us = UserStory(us_json)
    report.classify_user_story(us)

report.print_markdown()
