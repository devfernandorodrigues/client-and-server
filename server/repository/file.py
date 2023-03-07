import uuid
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

    def all(self):
        with open(self.file_path, "r") as f:
            try:
                return json.load(f)
            except JSONDecodeError:
                return {}

    def save(self, data):
        with open(self.file_path, "w") as f:
            json.dump(data, f, default=str)

    def get(self, _id):
        data = self.all()

        try:
            return data[_id]
        except KeyError:
            raise NotFound()

    def update(self, item):
        data = self.all()

        try:
            data[item["id"]] = item
        except KeyError:
            raise NotFound()

        self.save(data)

        return item

    def delete(self, _id):
        data = self.all()
        del data[_id]
        self.save(data)

    def create(self, item):
        data = self.all()
        item["id"] = str(uuid.uuid4())
        data[item["id"]] = item
        self.save(data)
        return item
