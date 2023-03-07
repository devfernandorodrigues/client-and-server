import requests
from models.item import Item


class ItemsClient:
    def __init__(self, base_url="http://localhost:8000"):
        self.base_url = base_url

    def _request(self, method, url, *args, **kwargs):
        headers = kwargs.get("headers", {})
        headers["Content-Type"] = "application/json"
        resp = requests.request(method, url, *args, headers=headers, **kwargs)
        resp.raise_for_status()
        return resp

    def items(self):
        resp = self._request("GET", f"{self.base_url}/items/")
        json_resp = resp.json()
        return [Item(**item) for item in json_resp]

    def create(self, item):
        resp = self._request(
            "POST", f"{self.base_url}/items/", data=item.json()
        )
        return Item(**resp.json())

    def read(self, _id):
        resp = self._request("GET", f"{self.base_url}/items/{_id}")
        return Item(**resp.json())

    def delete(self, item):
        self._request("DELETE", f"{self.base_url}/items/{item.id}")

    def update(self, item):
        resp = self._request(
            "PUT", f"{self.base_url}/items/{item.id}", data=item.json()
        )
        return Item(**resp.json())
