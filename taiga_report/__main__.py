"""Executes the report generator and updates the reported User Stories"""
from .taiga_api import TaigaAPI
from .classes import Report, UserStory, MarkdownPrinter, DocxPrinter


api = TaigaAPI("ignamt-sieel")
us_list = api.download_user_stories()

report = Report("SIEEL")

#TODO: Iterate over US
for us_json in us_list:
    us = UserStory(us_json)
    report.classify_user_story(us)

#MarkdownPrinter.print_markdown(report)
DocxPrinter.print_docx(report)
print("Success :)")


    