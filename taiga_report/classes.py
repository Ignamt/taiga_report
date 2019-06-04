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
        self.tags = us["tags"]
        self.subtasks = us["tasks"]
        if us["due_date"]:
            self.due_date = dt.datetime.strptime(us["due_date"],
                                                 "%Y-%m-%dT%H:%M:%S.%fZ")
        else:
            self.due_date = None


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
        self.sections = list()
        self.project = project
