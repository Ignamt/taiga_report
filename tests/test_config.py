import pytest
from tempfile import gettempdir
import yaml


@pytest.fixture
def yaml_path():
    yaml_dict = {
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
            ],
            'host': 'https://taiga.leafnoise.io/api/v1/',
            'login_data': {
                'type': 'normal',
                'username': 'ignamt',
                'password': 'tanoira1'
            }
        }
    }

    temp_yaml = gettempdir() + "test_dict.yaml"
    with open(temp_yaml, "w") as yaml_file:
        yaml.dump(yaml_dict, yaml_file, Dumper=yaml.Dumper)

    return temp_yaml


test_ProjectConfig():
    pass
