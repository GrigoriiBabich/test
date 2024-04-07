import json

class ItemsLoader:
    def load_items():
        with open("server/items.json", "r") as f:
            return json.load(f)