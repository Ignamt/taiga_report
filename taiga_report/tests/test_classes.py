"""Tests for classes.py."""
import pytest

from taiga_report import classes


@pytest.fixture
def report():
    yaml_dict = {
        'login_data': {
            'type': 'normal',
            'username': 'ignamt',
            'password': 'tanoira1'
        },
        'host': 'https://taiga.leafnoise.io/api/v1/',
        'headers': {
            'content-type': 'application/json',
            'x-disable-pagination': 'True'
        },
        'sieel': {
            'slug': 'ignamt-sieel',
            'id': 6,
            'done_id': 35,
            'report_sections': [
                'general',
                'expedientes',
                'remitos',
                'administracion'
            ]
        }
    }

    return classes.Report("sieel", yaml_dict)


@pytest.fixture
def us():
    us = {"subject": "Subject",
              "epics": [{"subject": "Epic"}],
              "tags": [["expedientes"]],
              "tasks": [],
              "due_date": None}
    return classes.UserStory(us)


class TestUserStoryClass():
    """UserStory class related tests."""

    def test_class_creation(self, us):
        """Tests creation of a UserStory instance."""
        assert us.subject == "Subject"
        assert us.epic == "Epic"
        assert us.tags == ["expedientes"]

    def test_userstory_section(self, us):
        us.tags = ["expedientes", "abm"]
        assert "abm" in us.tags
        assert us.section == "expedientes"


class TestReportClass:
    """Test Report creation and inner structure methods."""

    def test_class_creation(self, report):
        """Tests creation of a Report instance with attribute."""
        assert report.project == "SIEEL"

    def test_classify_section_not_in_report_no_epic(self, report, us):
        us.epic = ""
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["user_stories"]

    def test_classify_section_in_report_no_epic(self, report, us):
        us.epic = ""
        report._report["expedientes"] = {"user_stories": []}
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["user_stories"]

    def test_classify_section_not_in_report_with_epic(self, report, us):
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["Epic"]

    def test_classify_section_in_report_with_epic(self, report, us):
        report._report["expedientes"] = {"user_stories": []}
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["Epic"]

    def test_classify_epic_in_report(self, report, us):
        report._report["expedientes"] = {"user_stories": [],
                                         "Epic": []}
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["Epic"]


class TestReportPrinter:
    """Tests for the report printers"""
