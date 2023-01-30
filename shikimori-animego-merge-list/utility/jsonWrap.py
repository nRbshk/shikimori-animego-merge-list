import json


def saveJSON(path, content):
  with open(path, 'w') as save_file:
    json.dump(content, save_file, indent=2, ensure_ascii=False)


def loadJSON(path):
  with open(path, 'r') as load_file:
    return json.load(load_file)
