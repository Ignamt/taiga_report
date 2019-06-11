"""Executes the report generator and updates the reported User Stories."""
import yaml

from .taiga_api import TaigaAPI
from .classes import Report, UserStory

with open("taiga_report/api.yaml", "r") as yaml_file:
    yaml_dict = yaml.load(yaml_file)
    
api = TaigaAPI("sieel", yaml_dict)
us_list = api.download_user_stories()

report = Report("sieel", yaml_dict)

for us_json in us_list:
    us = UserStory(us_json)
    report.classify_user_story(us)

report.print_markdown()
