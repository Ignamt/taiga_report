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



