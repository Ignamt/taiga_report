class CLI:

    def __init__(self, config):
        # self.config = self._load_config(config)
        print("Welcome to the Taiga Report Command Line Interface.")
        self.options = {
            "1": {
                "text": "",
                "action": ""
            },
            "2": {
                "text": "",
                "action": ""
            }
        }


    def run(self):
        self.exit_cli = False
        while not exit_cli:
            self.main_loop()


    def main_loop(self):
        print("Select one of the following options:")


