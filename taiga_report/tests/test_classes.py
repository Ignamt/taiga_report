"""Tests for classes.py."""
import pytest
import datetime as dt
import docx

from taiga_report import classes
from docx import Document


@pytest.fixture
def document():
    document = Document()
    return document


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

    return classes.Report("sieel", yaml_dict)


@pytest.fixture
def us():
    """Create the us fixture."""
    us = {"subject": "Subject",
          "epics": [{"subject": "Epic"}],
          "tags": [["expedientes"]],
          "tasks": [],
          "due_date": None}
    return classes.UserStory(us)


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


class TestReportPrintMethods:
    """Tests for the report print methods."""

    def test_check_filename(self, report):
        """Test that the filename is created when it doesn't exist.

        Due to the dynamic nature of the file naming and useing the
        local directory to store the files, it's hard to do a good test.
        If this fails, just change the file version number."""
        year = dt.date.today().year
        month = str(dt.date.today().month).rjust(2, "0")
        ext = ".md"
        filename = "SIEEL_report_{}-{}".format(month, year) + ext
        assert report._check_filename(ext) == filename


class TestMarkdownPrinterClass:
    """Tests for the markdown printer class."""

    def test_md_title_creation(self):
        title = "foo title"
        md_title = "# {}\n\n".format(title)
        assert classes.MarkdownPrinter.md_title(title) == md_title

    def test_md_section_creation(self):
        section = "foo section".capitalize()
        md_section = "## {}\n\n".format(section)
        assert classes.MarkdownPrinter.md_section(section) == md_section

    def test_md_epic_creation(self):
        epic = "foo epic".capitalize()
        md_epic = "### {}\n\n".format(epic)
        assert classes.MarkdownPrinter.md_epic(epic) == md_epic

    def test_md_user_story_creation(self):
        user_story = "foo user_story".capitalize()
        md_user_story = "* {}\n".format(user_story)
        assert classes.MarkdownPrinter.md_user_story(
            user_story) == md_user_story


class TestDocxPrinterClass:
    """Tests for the docx printer class. 

    For now(and until a better argument is found)* the tests only checks the 
    creation of content in the Document.

    *: the Report class is already tested. All that the docx printer does is
    iterate over the report and create the title, sections, etc.   
    """

    def test_title_creation(self, document, report):
        title = classes.DocxPrinter.docx_title(document, report.project)
        assert isinstance(title, docx.text.paragraph.Paragraph)
        assert title.text == report.project.capitalize()
        assert title.style.name == "Title"

    def test_section_creation(self, document):
        generic_section = "foo section".capitalize()
        section = classes.DocxPrinter.docx_section(document, generic_section)
        assert isinstance(section, docx.text.paragraph.Paragraph)
        assert section.text == generic_section
        assert section.style.name == "Heading 1"

    def test_epic_creation(self, document):
        generic_epic = "foo epic".capitalize()
        epic = classes.DocxPrinter.docx_epic(document, generic_epic)
        assert isinstance(epic, docx.text.paragraph.Paragraph)
        assert epic.text == generic_epic
        assert epic.style.name == "Heading 5"

    def test_user_story_creation(self, document):
        generic_us = "foo us".capitalize()
        user_story = classes.DocxPrinter.docx_user_story(document, generic_us)
        assert isinstance(user_story, docx.text.paragraph.Paragraph)
        assert user_story.text == generic_us
        assert user_story.style.name == "List Bullet 2"
