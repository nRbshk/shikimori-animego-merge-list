import os
from pathlib import Path
from time import sleep

import requests
from utility.json import load_json, save_json
from animego import animego

from shikimori import collectShikimoriAnime


def main():
  Path('tmp').mkdir(exist_ok=True, parents=True)
  collected_shikimori_animes = [item.asJSON() for item in collectShikimoriAnime()]
  save_json(os.path.join('tmp', 'all_shikimori.json'), collected_shikimori_animes)

  # from_file = load_json(os.path.join('tmp', JSON_FILE_NAME))

  user = "siel_die"
  user_animeg_items = [item.asJSON() for item in animego.receiveItems(user)]
  save_json(os.path.join('tmp', user + "_animego.json"), user_animeg_items)


if __name__ == '__main__':
  main()
