from utility.animeItem import AnimeItem


def convert(item: AnimeItem, all_shikimore_items: list[AnimeItem]) -> AnimeItem:
  shiki_item = all_shikimore_items.get(item.target_title, None)
  if shiki_item is None:
    print("Could not convert anime:", item.target_title)
    return None
  convert_result = {}
  convert_result['target_title'] = item.target_title
  convert_result['target_title_ru'] = item.target_title_ru
  convert_result['target_id'] = shiki_item.get('target_id', None)
  convert_result['status'] = item.status
  convert_result['episodes'] = item.episodes
  if item.score is not None:
    convert_result['score'] = item.score
  return AnimeItem(**convert_result)
