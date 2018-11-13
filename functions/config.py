import json
from builtins import ValueError


CONFIG_FILE = 'config.json'


def create_config(data: dict):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=4)


def write_config(key: str, new_value):
    with open(CONFIG_FILE, 'r+') as f:
        json_data = json.load(f)
        json_data[key] = new_value

        f.seek(0)
        json.dump(json_data, f, indent=4)
        f.truncate()


def read_config(key: str) -> str:
    with open(CONFIG_FILE) as f:
        json_data = json.load(f)
        return json_data.get(key, None)


def increase_read_config(key: str) -> str:
    with open(CONFIG_FILE, 'r+') as f:
        json_data = json.load(f)
        try:
            data = int(json_data[key])
        except (IndexError, ValueError):
            return None

        json_data[key] = data + 1

        f.seek(0)
        json.dump(json_data, f, indent=4)
        f.truncate()

        return data + 1
