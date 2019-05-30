import datetime as dt


class UserStory:
    """Contains all the US info needed for the report."""
    def __init__(self, us):
        """Sets up attributes for the instance"""
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
        super().__init__()
        self.subject = subject


class Section:
    """Houses epics and US depending on predefined tags."""
    def __init__(self, name):
        self.name = name
        self.epics = list()
        self.user_stories = list()

class Report:
    """Gathers all sections and prints itself in various formats"""
    def __init__(self):
        self.sections = list()

