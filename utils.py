import collections
import json


class Storage(collections.UserDict):
    """https://docs.python.org/3.8/library/collections.html?highlight=userdict#collections.UserDict"""

    def __setitem__(self, *args, **kwargs):
        super().__setitem__(*args, **kwargs)

        with open(self.path, 'w') as f:
            json.dump(self.data, f)

    def init_data(self, path):
        self.path = path

        try:
            with open(self.path, 'r') as f:
                self.data = json.load(f)
        except (OSError, json.decoder.JSONDecodeError):  # File not exists or empty
            self.data = {}

    def get_all(self):
        return self.data


storage = Storage()
