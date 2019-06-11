"""Contains classes for the different sections of the report."""
import datetime as dt
from pathlib import Path


class UserStory:
    """Contains all the US info needed for the report."""

    def __init__(self, us):
        """Set up attributes for the instance.
        
        Parameters:
        - us: Dict with all the info that comes from the Taiga
              API"""
        self.subject = us["subject"]
        self.epic = us["epics"][0]["subject"] if us["epics"] else []
        self.tags = us["tags"][0] if us["tags"] else []
        self.section = self._section
        self.subtasks = us["tasks"]
        # if us["due_date"]:
        #     self.due_date = dt.datetime.strptime(us["due_date"],
        #                                          "%Y-%m-%dT%H:%M:%S.%fZ")
        # else:
        #     self.due_date = None

    @property
    def _section(self):
        for tag in self.tags:
            if tag in ["general", "expedientes", "remitos", "administracion"]:
                return tag
            else:
                return None
        


class Epic(list):
    """Gathers the US and task subjects related to a certain epic."""

    def __init__(self, subject):
        """Set up attributes for the instance."""
        super().__init__()
        self.subject = subject
        self.user_stories = list()


class Section:
    """Houses epics and US depending on predefined tags."""

    def __init__(self, name):
        """Set up attributes for the instance."""
        self.name = name.capitalize()
        self.epics = list()
        self.user_stories = list()


class Report:
    """Gathers all sections and prints itself in various formats."""

    def __init__(self, project):
        """Set up attributes for the instance."""
        self._report = dict()
        self.project = project
        self._report_sections = ["general", "expedientes", "remitos", "administracion"]

    def classify_user_story(self, us):
        if us.section not in self._report:
            self._report[us.section] = {"user_stories": []}
            section = self._report[us.section]
            if us.epic:
                section[us.epic] = [us.subject]
            else:
                section["user_stories"].append(us.subject)
        else:
            if not us.epic:
                self._report[us.section]["user_stories"].append(us.subject)

            elif us.epic not in self._report[us.section]:
                self._report[us.section].update({us.epic: [us.subject]})

            else:
                self._report[us.section][us.epic].append(us.subject)

    def _check_filename(self):
        year = dt.date.today().year
        month = dt.date.today().month
        filename = self.project + "_report_{}-{}".format(month, year)
        if Path(filename+".md").is_file():
            filename += "_1"
        while Path(filename+".md").is_file():
            filename = filename.replace(filename[-1], str(int(filename[-1])+1))
        filename += ".md"
        return filename

    def print_markdown(self):
        filename = self._check_filename()
        with open(filename, "a+") as file:
            file.write(md_title(self.project))
            for section in self._report_sections:
                if section in self._report:
                    self._print_section_md(section, file)
                

    def _print_section_md(self, section, file):
        file.write(md_section(section))
        rep_section = self._report[section]
        if rep_section.get("user_stories"):
                self._print_userstories_md(rep_section["user_stories"], file)
        
        for epic in self._report[section]:
            if epic == "user_stories":
                continue
            
            self._print_epic_md(section, epic, file)

    def _print_epic_md(self, section, epic, file):
        file.write(md_epic(epic))
        self._print_userstories_md(self._report[section][epic], file)

    def _print_userstories_md(self, userstories, file):
        for us in userstories:
            file.write(md_user_story(us))
        # Add one final newline to separate from other parts of the report
        file.write("\n")





def md_title(content):
    return "# {}\n\n".format(content)


def md_section(content):
    return "## {}\n\n".format(content.capitalize())


def md_epic(content):
    return "### {}\n\n".format(content.capitalize())


def md_user_story(content):
    return "* {}\n".format(content.capitalize())
