
import datetime as dt

import pytest
import docx
from docx import Document

from taiga_report import report_classes as rc
from taiga_report import printer_classes as pc


@pytest.fixture
def document():
    """Set up mock Document() object."""
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

    return rc.Report("sieel", yaml_dict)


class TestBasePrinterMethods:
    """Tests for the report print methods."""

    def test_check_filename_md(self, report):
        """Test that the filename is created when it doesn't exist.

        Due to the dynamic nature of the file naming and useing the
        local directory to store the files, it's hard to do a good test.
        If this fails, just change the file version number.

        """
        year = dt.date.today().year
        month = str(dt.date.today().month).rjust(2, "0")
        ext = ".md"
        filename = "SIEEL_report_{}-{}".format(month, year) + ext
        assert pc.MarkdownPrinter._check_filename(report.project) == filename


    def test_check_filename_docx(self, report):
        """Test that the filename is created when it doesn't exist.

        Due to the dynamic nature of the file naming and useing the
        local directory to store the files, it's hard to do a good test.
        If this fails, just change the file version number.

        """
        year = dt.date.today().year
        month = str(dt.date.today().month).rjust(2, "0")
        ext = ".docx"
        filename = "SIEEL_report_{}-{}".format(month, year) + ext
        assert pc.DocxPrinter._check_filename(report.project) == filename

    def test_Printer_check_filename_raises_exception(self, report):
        """Test that the base class function raises an exception."""
        with pytest.raises(Exception):
            pc.Printer._check_filename(report.project)


class TestMarkdownPrinterClass:
    """Tests for the markdown printer class.

    For now(and until a better argument is found)* the tests only check the
    creation of content in the markdown.

    *: the Report class is already tested. All that the markdown printer does
    is iterate over the report and create the title, sections, etc.

    """

    def test_md_title_creation(self):
        """Test that output is as expected."""
        title = "foo title"
        md_title = "# {}\n\n".format(title)
        assert pc.MarkdownPrinter.md_title(title) == md_title

    def test_md_section_creation(self):
        """Test that output is as expected."""
        section = "foo section".capitalize()
        md_section = "## {}\n\n".format(section)
        assert pc.MarkdownPrinter.md_section(section) == md_section

    def test_md_epic_creation(self):
        """Test that output is as expected."""
        epic = "foo epic".capitalize()
        md_epic = "### {}\n\n".format(epic)
        assert pc.MarkdownPrinter.md_epic(epic) == md_epic

    def test_md_user_story_creation(self):
        """Test that output is as expected."""
        user_story = "foo user_story".capitalize()
        md_user_story = "* {}\n".format(user_story)
        assert pc.MarkdownPrinter.md_user_story(
            user_story) == md_user_story


class TestDocxPrinterClass:
    """Tests for the docx printer class.

    For now(and until a better argument is found)* the tests only checks the
    creation of content in the Document.

    *: the Report class is already tested. All that the docx printer does is
    iterate over the report and create the title, sections, etc.

    """

    def test_title_creation(self, document, report):
        """Test that output is as expected."""
        title = pc.DocxPrinter.docx_title(document, report.project)
        assert isinstance(title, docx.text.paragraph.Paragraph)
        assert title.text == report.project.capitalize()
        assert title.style.name == "Title"

    def test_section_creation(self, document):
        """Test that output is as expected."""
        generic_section = "foo section".capitalize()
        section = pc.DocxPrinter.docx_section(document, generic_section)
        assert isinstance(section, docx.text.paragraph.Paragraph)
        assert section.text == generic_section
        assert section.style.name == "Heading 1"

    def test_epic_creation(self, document):
        """Test that output is as expected."""
        generic_epic = "foo epic".capitalize()
        epic = pc.DocxPrinter.docx_epic(document, generic_epic)
        assert isinstance(epic, docx.text.paragraph.Paragraph)
        assert epic.text == generic_epic
        assert epic.style.name == "Heading 5"

    def test_user_story_creation(self, document):
        """Test that output is as expected."""
        generic_us = "foo us".capitalize()
        user_story = pc.DocxPrinter.docx_user_story(document, generic_us)
        assert isinstance(user_story, docx.text.paragraph.Paragraph)
        assert user_story.text == generic_us
        assert user_story.style.name == "List Bullet 2"
