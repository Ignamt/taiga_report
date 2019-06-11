"""Tests for classes.py."""
import pytest

from taiga_report import classes


@pytest.fixture
def report():
    return classes.Report("SIEEL")


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


class TestEpicClass:
    """Epic class related tests."""

    def test_class_creation(self):
        """Tests creation of an Epic instance."""
        epic = classes.Epic("expedientes")


class TestSectionClass:
    """Section class related tests."""

    def test_class_creation(self):
        """Tests creation of a Section instance."""
        section = classes.Section(name="expedientes")



class TestReportClass:
    """Test Report creation and inner structure methods."""

    def test_class_creation(self):
        """Tests creation of a Report instance with attribute."""
        report = classes.Report("SIEEL")
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
