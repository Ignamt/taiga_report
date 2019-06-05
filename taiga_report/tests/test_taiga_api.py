"""Tests for the TaigaAPI"""
from unittest import TestCase
from taiga_report import taiga_api


class TestAPI(TestCase):
    """Contains tests for the API class and methods"""


    def setUp(self):
        self.api = taiga_api.TaigaAPI("ignamt-sieel")


    def test_api_creation(self):
        self.assertEqual(self.api.slug, "ignamt-sieel")
        self.assertEqual(self.api.host,
                         "https://taiga.leafnoise.io/api/v1/")
        self.assertEqual(self.api.auth_url,
                         "https://taiga.leafnoise.io/api/v1/auth")
        self.assertEqual(self.api.headers,
                         {"content-type": "application/json",
                          "x-disable-pagination": "True"})

    def test_login(self):
        login_data = self.api._login()
        self.assertEqual(login_data["username"], "ignamt")

    def test_save_auth(self):
        auth_token = "testauthtoken"
        self.api._save_auth(auth_token, os.sep.join(["taiga_report", "tests", "test_config.py"]))

        import taiga_report.tests.test_config as config
        self.assertEqual(config.TEST_AUTH_TOKEN, "testauthtoken")

    
    def test_auth(self):
        pass
