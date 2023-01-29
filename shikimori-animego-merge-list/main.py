from pathlib import Path
from utility.json import load_json, save_json
from animego import animego
import os
from shikimori import shikimori
from utility.toShikimori import convert
from utility.animeItem import AnimeItem
USER_SHIKIMORI = "madeinheavens"
USER_ANIMEGO = "siel_die"


def collectAnimegoUserAnime(user: str = USER_ANIMEGO):
  user_animego_items = animego.collectByUser(USER_ANIMEGO)
  filename = os.path.join('tmp', user + "_animego.json")
  save_json(filename, [item.asJSON() for item in user_animego_items])
  filename_map = os.path.join('tmp', user + "_animego_map.json")
  return user_animego_items


def collectAllShikimoriAnime():
  collected_shikimori_animes = shikimori.collectShikimoriAnime()
  map_collected_shikimori_animes = {}
  for shikimori_anime in collected_shikimori_animes:
    map_collected_shikimori_animes[shikimori_anime.target_title] = shikimori_anime.asJSON()
  filename = os.path.join('tmp', 'all_shikimori.json')
  save_json(filename, map_collected_shikimori_animes)
  return collectAllShikimoriAnime


def collectShikimoriUserAnime(user: str = USER_SHIKIMORI):
  user_shikimori_items = shikimori.collectByUser(user)
  filename = os.path.join('tmp', user + "_shikimori.json")
  save_json(filename, [item.asJSON() for item in user_shikimori_items])
  return user_shikimori_items


def convertAnimegoToShikimori(user) -> list[AnimeItem]:
  user_animego_items_path = os.path.join('tmp', user + '_animego.json')
  if not os.path.exists(user_animego_items_path):
    raise Exception("Could not found " + user_animego_items_path + "\nUse collectAnimegoUserAnime function before convert")
  all_shikimori_path = os.path.join('tmp', 'all_shikimori.json')
  if not os.path.exists(user_animego_items_path):
    raise Exception("Could not found " + all_shikimori_path + "\nUse collectAllShikimoriAnime function before convert")

  converted_items = []
  not_converted_items = []
  all_shikimori_items = load_json(all_shikimori_path)
  for animego_item in load_json(user_animego_items_path):
    anime_item = AnimeItem(**animego_item)
    converted_item = convert(anime_item, all_shikimori_items)
    if not converted_item:
      not_converted_items.append(anime_item.asJSON())
      continue
    converted_items.append(converted_item)

  save_json(os.path.join('tmp', user + '_animego_converted.json'), [item.asJSON() for item in converted_items])
  save_json(os.path.join('tmp', user + '_animego_not_converted.json'), not_converted_items)

  return converted_items


def mergeAnimegoWithShikimori(user_animego: str = USER_ANIMEGO, user_shikimori: str = USER_SHIKIMORI, leading_animego: bool = True):
  def withLeading(animego_item, shikimori_item, field, leading_animego: bool = True):
    if leading_animego:
      return animego_item.get(field) or shikimori_item.get(field)
    return shikimori_item.get(field) or animego.get(field)

  converted_animego_user_path = os.path.join("tmp", user_animego + "_animego_converted.json")
  if not os.path.exists(converted_animego_user_path):
    raise Exception("Could not found " + converted_animego_user_path + "\nUse convertAnimegoToShikimori function before merge")
  shikimori_user_path = os.path.join("tmp", user_shikimori + "_shikimori.json")
  if not os.path.exists(shikimori_user_path):
    raise Exception("Could not found " + shikimori_user_path + "\nUse collectShikimoriUserAnime function before merge")

  animego_converted_user_animes = load_json(converted_animego_user_path)
  shikimori_user_animes = load_json(shikimori_user_path)
  shikimori_user_animes_map = {}
  for shikimori_anime in shikimori_user_animes:
    shikimori_user_animes_map[shikimori_anime.get('target_title')] = shikimori_anime

  merged_items = []
  for animego_item in animego_converted_user_animes:
    target_title = animego_item.get("target_title")
    shikimori_item = shikimori_user_animes_map.get(target_title, {})
    target_id = animego_item.get('target_id')
    score = withLeading(animego_item, shikimori_item, 'score', leading_animego) or None
    episodes = withLeading(animego_item, shikimori_item, 'episodes', leading_animego) or 0
    status = withLeading(animego_item, shikimori_item, 'status', leading_animego)
    merged_items.append({
        'target_title': target_title,
        'target_id': target_id,
        'score': score,
        'episodes': episodes,
        'status': status,
        'target_type': 'Anime'
    })
  save_json(os.path.join('tmp', "merged.json"), merged_items)


def main():
  Path('tmp').mkdir(exist_ok=True, parents=True)
  convertAnimegoToShikimori(USER_ANIMEGO)
  collectShikimoriUserAnime(USER_SHIKIMORI)
  mergeAnimegoWithShikimori(USER_ANIMEGO, USER_SHIKIMORI)
  # collected_shikimori_animes = shikimori.collectShikimoriAnime()
  # map_collected_shikimori_animes = {}
  # for shikimori_anime in collected_shikimori_animes:
  #   map_collected_shikimori_animes[shikimori_anime.target_title] = shikimori_anime.asJSON()
  # save_json(os.path.join('tmp', 'all_shikimori.json'), map_collected_shikimori_animes)

  # user_shikimori_items = shikimori.collectByUser(USER_SHIKIMORI)
  # [print(i) for i in user_shikimori_items]

  # user_animego_items = animego.collectByUser(USER_ANIMEGO)
  # [print(i) for i in user_animego_items]

  # all_shikimori_items = load_json(os.path.join('tmp', 'all_shikimori.json'))
  # for animego_item in user_animego_items:
  #   convertToShikimori(animego_item, all_shikimori_items)
  # shikimori_all_items = load_json(os.path.join("tmp", "all_shikimori.json"))
  # user_animego_items = animego.collectByUser(USER_ANIMEGO)
  # converted_items = []
  # for animego_item in user_animego_items:
  #   converted_item = convert(animego_item, shikimori_all_items)
  #   if converted_item is None:
  #     continue
  #   converted_items.append(converted_item.asJSON())
  # save_json(os.path.join('tmp', USER_ANIMEGO + '_animego_converted.json'), converted_items)
  # save_json(os.path.join('tmp', USER_ANIMEGO + "_animego.json"), user_animego_items)

  # collected_animego_animes = [item.asJSON() for item in animego.collectAnime()]
  # save_json(os.path.join('tmp', 'all_animego.json'), collected_animego_animes)


if __name__ == '__main__':
  main()
