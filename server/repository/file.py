import json
from json import JSONDecodeError
import os

from pathlib import Path


class NotFound(Exception):
    pass


class FileRepository:
    def __init__(self):
        repository_path = Path(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = repository_path.parent / "db" / "items.json"

    def read(self):
        with open(self.file_path, "r") as f:
            try:
                return json.load(f)
            except JSONDecodeError:
                return []

    def save(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, default=str)

    def get(self, _id):
        data = self.read()
        item = [d for d in data if d["id"] == _id]
        if len(item) == 0:
            raise NotFound()
        return item[0]

    def update(self, item):
        data = self.read()

        for i, d in enumerate(data):
            if item.id == d["id"]:
                break
        else:
            raise NotFound()

        data.pop(i)

        data.insert(i, item)

        self.save(data)

        return item

    def delete(self, _id):
        data = self.read()

        for i, d in enumerate(data):
            if _id == d["id"]:
                break
        else:
            raise NotFound()

        data.pop(i)

        self.save(data)
