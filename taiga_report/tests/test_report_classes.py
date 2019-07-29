"""Tests for classes.py."""
import datetime as dt

import pytest
import docx

from taiga_report import report_classes as rc


@pytest.fixture
def report():
    """Create a report fixture."""
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

    return rc.Report("sieel", yaml_dict)


@pytest.fixture
def us():
    """Create the us fixture."""
    us = {"subject": "Subject",
          "epics": [{"subject": "Epic"}],
          "tags": [["expedientes"]],
          "tasks": [],
          "due_date": None}
    return rc.UserStory(us)


class TestUserStoryClass():
    """UserStory class related tests."""

    def test_class_creation(self, us):
        """Test creation of a UserStory instance."""
        assert us.subject == "Subject"
        assert us.epic == "Epic"
        assert us.tags == ["expedientes"]

    def test_userstory_section(self, us):
        """Test that the US gets the specified sections only."""
        us.tags = ["expedientes", "abm"]
        assert "abm" in us.tags
        assert us.section == "expedientes"


class TestReportClass:
    """Test Report creation and inner structure methods."""

    def test_class_creation(self, report):
        """Tests creation of a Report instance with attribute."""
        assert report.project == "SIEEL"

    def test_classify_section_not_in_report_no_epic(self, report, us):
        """Test US classified correctly if new section and has no epic."""
        us.epic = ""
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["user_stories"]

    def test_classify_section_in_report_no_epic(self, report, us):
        """Test US classified correctly if existing section and has no epic."""
        us.epic = ""
        report._report["expedientes"] = {"user_stories": []}
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["user_stories"]

    def test_classify_section_not_in_report_with_epic(self, report, us):
        """Test US classified correctly if new section and has epic."""
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["Epic"]

    def test_classify_section_in_report_with_epic(self, report, us):
        """Test US classified correctly if existing section and has epic."""
        report._report["expedientes"] = {"user_stories": []}
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["Epic"]

    def test_classify_epic_in_report(self, report, us):
        """Test US classified correctly if epic already in report."""
        report._report["expedientes"] = {"user_stories": [],
                                         "Epic": []}
        report.classify_user_story(us)
        assert "Subject" in report._report["expedientes"]["Epic"]

