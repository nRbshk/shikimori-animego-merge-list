import json


def save_json(path, content):
  with open(path, 'w') as save_file:
    json.dump(content, save_file, indent=4, ensure_ascii=False)


def load_json(path):
  with open(path, 'r') as load_file:
    return json.load(load_file)
