"""Tests for classes.py."""
from unittest import TestCase
from taiga_report import classes


class TestUserStoryClass(TestCase):
    def test_class_creation(self):
        us = {"subject": "Prueba de Clase",
              "epics": [{"subject": "Test Case"}],
              "tags": ["expedientes"],
              "tasks": [],
              "due_date": None}

        userstory = classes.UserStory(us)


class TestEpicClass(TestCase):
    pass


class TestSectionClass(TestCase):
    pass


class TestReportClass(TestCase):
    pass
