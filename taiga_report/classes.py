"""Contains classes for the different sections of the report."""
import datetime as dt


class UserStory:
    """Contains all the US info needed for the report."""

    def __init__(self, us):
        """Set up attributes for the instance.
        
        Parameters:
        - us: Dict with all the info that comes from the Taiga
              API"""
        self.subject = us["subject"]
        self.epic = us["epics"][0]["subject"]
        self.tags = us["tags"][0]
        self.section = self._section
        self.subtasks = us["tasks"]
        if us["due_date"]:
            self.due_date = dt.datetime.strptime(us["due_date"],
                                                 "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            self.due_date = None

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

    def print_markdown(self):
        filename = self.project + "_report.md"
        with open(filename, "a+") as file:
            file.write(title(self.project))
            for section in self._report_sections:
                self._print_section_md(section, file)
                

    def _print_section_md(self, section, file):
        file.write(section())



def md_title(content):
    return "# {}\n\n".format(content)


def md_section(content):
    return capitalize("## {}\n\n".format(content))


def md_epic(content):
    return capitalize("### {}\n\n".format(content))


def md_user_story(content):
    return capitalize("* {}\n".format(content))
