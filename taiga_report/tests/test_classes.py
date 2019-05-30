"""Tests for classes.py."""
from unittest import TestCase
from taiga_report import classes


class TestUserStoryClass(TestCase):
    """UserStory class related tests"""

    def test_class_creation(self):
        """Tests creation of a UserStory instance."""
        us = {"subject": "Prueba de Clase",
              "epics": [{"subject": "Test Case"}],
              "tags": ["expedientes"],
              "tasks": [],
              "due_date": None}

        userstory = classes.UserStory(us)


class TestEpicClass(TestCase):
    """Epic class related tests."""
    
    def test_class_creation(self):
        """Tests creation of an Epic instance"""
        epic = classes.Epic("expedientes")


class TestSectionClass(TestCase):
    """Section class related tests."""
    def test_class_creation(self):
        """Tests creation of a Section instance"""
        section = classes.Section()


class TestReportClass(TestCase):
    """Report class related tests"""
    def test_class_creation(self):
        """Tests creation of a Report instance with attribute"""
        report = classes.Report()
        self.assertTrue(hasattr(report, "sections"))
