"""Executes the report generator and updates the reported User Stories"""
from taiga_api import TaigaAPI
from classes import Report, UserStory


api = TaigaAPI("ignamt-sieel")
us_list = api.download_user_stories()

report = Report("SIEEL")

#TODO: Iterate over US
for us_json in us_list:
    us = UserStory(us_json)
    report.classify_user_story(us)
    #TODO: Check for section tag
        #TODO: Add to section if exists or create if not

    #TODO: Check for epic
        #TODO: Add to epic if exists or create if no

    