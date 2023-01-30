import animego
import shikimori
import os
from utility.animeItem import AnimeItem
from typing import Callable
from utility import groupBy, withLeading, jsonWrap

class Converter:
  _instance = None
  TARGET_TYPE = 'Anime'
  SHIKIMORI_API_URL = 'https://shikimori.one/api/animes'
  ANIMEGO_API_URL = 'https://animego.org/anime'


  def __new__(cls):
    if cls._instance is None:
      cls._instance = super(Converter, cls).__new__(cls)
    return cls._instance

  @staticmethod
  def __baseCollect(source: str, filename: str, collect: Callable) -> list[AnimeItem]:
    collection: list[AnimeItem] = collect(source)
    print(filename)
    jsonWrap.saveJSON(filename, [item.asJSON() for item in collection])
    return collection

  @staticmethod
  def collectAnimegoUserAnime(user: str) -> list[AnimeItem]:
    return Converter.__baseCollect(user, f'tmp/{user}_animego.json', animego.collectByUser)

  @staticmethod
  def collectShikimoriUserAnime(user: str) -> list[AnimeItem]:
    return Converter.__baseCollect(user, f'tmp/{user}_shikimori.json', shikimori.collectByUser)

  @staticmethod
  def collectAllShikimoriAnime(api_url: str = SHIKIMORI_API_URL) -> list[AnimeItem]:
    return Converter.__baseCollect(api_url, 'tmp/all_shikimori.json', shikimori.collectAll)

  @staticmethod
  def collectAllAnimegoAnime(api_url: str = ANIMEGO_API_URL) -> list[AnimeItem]:
    return Converter.__baseCollect(api_url, 'tmp/all_animego.json', animego.collectAll)

  @staticmethod
  def __baseConvert(item: AnimeItem, other_items: dict[str, object]) -> AnimeItem:
    other_item = other_items.get(item.target_title, other_items.get(item.target_title_ru, None))
    if not other_item:
      print("Could not convert anime item:", item.target_title)
      return None
    other_item = AnimeItem(**other_item)
    result = {
        'target_title': item.target_title,
        'target_title_ru': item.target_title_ru,
        'target_id': item.target_id or other_item.target_id,
        'status': item.status,
        'episodes': item.episodes
    }
    if item.score is not None:
      result['score'] = item.score
    return AnimeItem(**result)

  @staticmethod
  def convertAnimegoToShikimori(user: str) -> list[AnimeItem]:
    user_items_path = os.path.join('tmp', user + '_animego.json')
    if not os.path.exists(user_items_path):
      raise Exception("Could not found " + user_items_path + "\nUse collectAnimegoUserAnime function before convert")
    all_shikimori_path = os.path.join('tmp', 'all_shikimori.json')
    if not os.path.exists(user_items_path):
      raise Exception("Could not found " + all_shikimori_path + "\nUse collectAllShikimoriAnime function before convert")

    converted_items = []
    not_converted_items = []
    all_shikimori_items = groupBy(jsonWrap.loadJSON(all_shikimori_path), 'target_title')

    for item in jsonWrap.loadJSON(user_items_path):
      item = AnimeItem(**item)
      converted = Converter.__baseConvert(item, all_shikimori_items)
      if not converted:
        not_converted_items.append(item.asJSON())
        continue
      converted_items.append(converted)

    jsonWrap.saveJSON(os.path.join('tmp', user + '_animego_converted.json'), [item.asJSON() for item in converted_items])
    jsonWrap.saveJSON(os.path.join('tmp', user + '_animego_not_converted.json'), not_converted_items)

    return converted_items

  @staticmethod
  def __baseMerge(left: object, right: object, merge_order: bool) -> object:
    return {
      'target_title': left.get('target_title'),
      'target_id': left.get('target_id'),
      'score': withLeading(left, right, 'score', merge_order) or None,
      'episodes': withLeading(left, right, 'episodes', merge_order) or 0,
      'status': withLeading(left, right, 'status', merge_order),
      'target_type': Converter.TARGET_TYPE
    }
  @staticmethod
  def __baseMergeLists(converted_filename: str, merge_with_filename: str, merge_order: bool = False) -> None:
    if not os.path.exists(converted_filename):
      raise Exception(
          "Could not found " +
          converted_filename +
          "\nUse convertShikimoriToAnimego or convertAnimegoToShikimori function before merge")
    if not os.path.exists(merge_with_filename):
      raise Exception(
          "Could not found " +
          merge_with_filename +
          "\nUse collectShikimoriUserAnime or collectAnimegoUserAnime function before merge")
    converted_items = jsonWrap.loadJSON(converted_filename)
    merge_with_items = groupBy(jsonWrap.loadJSON(merge_with_filename), 'target_title')
    merged_items = []
    for converted_item in converted_items:
      merge_item = merge_with_items.get(converted_item.get('target_title'), {})
      merged_items.append(Converter.__baseMerge(converted_item, merge_item, merge_order))
    jsonWrap.saveJSON(os.path.join('tmp', "merged.json"), merged_items)

  @staticmethod
  def mergeAnimegoWithShikimori(user_animego: str, user_shikimori: str, leading_animego: bool = True) -> None:
    Converter.__baseMergeLists(
        os.path.join('tmp', f'{user_animego}_animego_converted.json'),
        os.path.join('tmp', f'{user_shikimori}_shikimori.json'),
        leading_animego)

  @staticmethod
  def mergeShikimoriWithAnimego(user_shikimori: str, user_animego: str, leading_shikimori: bool = True) -> None:
    raise NotImplementedError("Method not implemented as animego has no upload functionality!")