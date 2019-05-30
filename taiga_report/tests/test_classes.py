"""Tests for classes.py."""
from unittest import TestCase
import classes


class TestUserStoryClass(TestCase):
    def test_class_creation(self):
        us = classes.UserStory()

    def test_creation_without_input(self):
        with self.assertRaises(AttributeError):
            us = classes.UserStory()
