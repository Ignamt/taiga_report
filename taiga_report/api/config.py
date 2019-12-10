import yaml


class Config:

    def __init__(self, yaml_path):

        headers, projects = self.load_yaml(yaml_path)
        self.headers = headers
        self.projects = [k for k in projects.keys()]
        for k, v in projects.items():
            setattr(self, k, ProjectConfig(**v)


    def load_yaml(cls, yaml_path):
        with open(yaml_path, "r") as yaml_file:
            yaml_dict = yaml.load(yaml_file, Loader=yaml.FullLoader)

        headers = yaml_dict.get("headers")
        projects = [{k: v} for k, v in yaml_dict.items() if k != "headers"]

        return headers, projects





class ProjectConfig:

    def __init__(slug: str, id: int, done_id: int, report_sections: dict,
                 host: str, login_data: dict):
        self.slug = slug
        self.id = id,
        self.done_id = done_id
        self.report_sections = report_sections
        self.host = host
        self.login_data = login_data
        

