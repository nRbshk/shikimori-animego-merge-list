import requests
from time import sleep
from utility import AnimeItem
SHIKIMORI_URL_API = 'https://shikimori.one/api/animes'
HEADERS = {
    "Connection": "keep-alive",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36"
}


def collectShikimoriAnime(url: str = SHIKIMORI_URL_API) -> list[AnimeItem]:
  shikimori_anime: list[AnimeItem] = []
  while True:
    page_index = (len(shikimori_anime) // 50) + 1
    response = requests.get(url, headers=HEADERS, params={'limit': 50, 'page': page_index})
    if not response.ok:
      print('\n'.join(['Reached maximum limits of requests to ' + response.url, 'Waiting 10 sec for unblock IP']))
      sleep(10)
      continue
    if len(response.json()) == 0:
      print(f'Fetched all anime from the shikimori. Last page was {page_index}')
      break

    for anime in response.json():
      name, russian, episodes, id = anime.get('name'), anime.get('russian'), anime.get('episodes'), anime.get('id')
      shikimori_anime.append(AnimeItem(name, russian, episodes, id, None))
    sleep(0.44)

  return shikimori_anime
