"""Executes the report generator and updates the reported User Stories."""
import yaml

from .taiga_api import TaigaAPI
from .classes import Report, UserStory, MarkdownPrinter, DocxPrinter

with open("taiga_report/api.yaml", "r") as yaml_file:
    yaml_dict = yaml.load(yaml_file)
    
api = TaigaAPI("sieel", yaml_dict)
us_list = api.download_user_stories()

report = Report("sieel", yaml_dict)

for us_json in us_list:
    us = UserStory(us_json)
    report.classify_user_story(us)

<<<<<<< HEAD
report.print_markdown()
=======
#MarkdownPrinter.print_markdown(report)
DocxPrinter.print_docx(report)
print("Success :)")


    
>>>>>>> Added MarkdownPrinter and DocxPrinter.
