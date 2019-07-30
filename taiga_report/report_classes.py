"""Contains classes for the different sections of the report."""
# import datetime as dt


class UserStory:
    """Contains all the US info needed for the report."""

    def __init__(self, us):
        """Set up attributes for the instance.

        Parameters:
        - us: Dict with all the info that comes from the Taiga
            API

        """
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


class Report:
    """Gathers all sections and prints itself in various formats."""

    def __init__(self, project, yaml_dict):
        """Set up attributes for the instance."""
        self._report = dict()
        self.project = project.upper()
        self._report_sections = yaml_dict[project]["report_sections"]

    def classify_user_story(self, us):
        """Classify a US and store it in the report json.

        PARAMETERS:
            - us: UserStory() object

        EXAMPLE OF REPORT JSON:
        report = {
            "section-1": {
                "user_stories": ["US-1", "US-2"],
                "epic-1": ["US-3", "US-4"]
                "epic-2": ["US-5", "US-6"]
            },
            "section-2": {
                "user_stories": ["US-7", "US-8"]
            }
        }

        """
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
