import os
from pathlib import Path
from time import sleep

import requests
from utility.json import load_json, save_json


JSON_FILE_NAME = 'anime_shikimori.json'

SHIKIMORI_URL_API = 'https://shikimori.one/api/animes'
HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"
}


def collect_shikimori_anime(url, json_file):

  shikimori_anime = []
  while True:
    page_index = (len(shikimori_anime) // 50) + 1
    response = requests.get(url, headers=HEADERS, params={'limit': 50, 'page': page_index})

    if response.ok:
      print('\n'.join(['Reached maximum limits of requests to ' + response.url, 'Waiting 10 sec for unblock IP']))
      sleep(10)
      continue
    if len(response.json()) == 0:
      print(f'Fetched all anime from the shikimori. Last page was {page_index}')
      break

    for anime in response.json():
      shikimori_anime.append({
          'name': anime.get('name'),
          'russian': anime.get('russian'),
          'episodes': anime.get('episodes'),
          'id': anime.get('id')

      })
    sleep(0.44)
  if os.path.exists('tmp'):
    os.remove('tmp')
  Path('tmp').mkdir(exist_ok=True, parents=True)
  save_json(os.path.join('tmp', json_file), shikimori_anime)

  return shikimori_anime


# def get_animego_mylist(user):
#   animego_anime = []
#   base_url = f'https://animego.org/user/{user}/mylist/anime'
#   while True:
#     page_index = len(animego_anime) + 1
#     page_0 = requests.get(base_url, headers=HEADERS)
#     break


def main():
  shikimoris_anime = collect_shikimori_anime(SHIKIMORI_URL_API, JSON_FILE_NAME)
  from_file = load_json(os.path.join('tmp', JSON_FILE_NAME))

  # print(len(from_file))
  # get_animego_mylist('siel_die')


if __name__ == '__main__':
  main()
