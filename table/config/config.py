import json


class Config:
    def __init__(self, path: str):
        self.path = path
        with open(path, "r") as f:
            self.data = json.load(f)

    def output(self):
        print(self.data)
