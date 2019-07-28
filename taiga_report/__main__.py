"""Executes the report generator and updates the reported User Stories."""
import yaml

from .taiga_api import TaigaAPI
from .classes import Report, UserStory, MarkdownPrinter, DocxPrinter

with open("taiga_report/api.yaml", "r") as yaml_file:
    yaml_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)

project = "sieel"  # TODO: Make it parameterized via CLI, bot or front-end
api = TaigaAPI(project, yaml_dict)
us_list = api.download_user_stories()

report = Report(project, yaml_dict)

for us_json in us_list:
    us = UserStory(us_json)
    report.classify_user_story(us)

# MarkdownPrinter.print_markdown(report)
DocxPrinter.print_docx(report)
print("Success :)")
