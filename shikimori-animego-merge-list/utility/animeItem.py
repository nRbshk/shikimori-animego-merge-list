

class AnimeItem:
  def __init__(self, **kwargs):
    self.target_title = kwargs.get("target_title", "")
    self.target_title_ru = kwargs.get("target_title_ru", None)
    self.target_id = kwargs.get("target_id", None)
    episodes = kwargs.get("episodes", 0)
    self.episodes = 0 if episodes == '–' else episodes
    score = kwargs.get('score', None)
    self.score = None if type(score) == 'str' and score.strip() == '–' else score
    self.status = AnimeItem.convertStatus(kwargs.get("status", ""))

  def asJSON(self) -> dict[str, str]:
    basic_json = {
        'target_title': self.target_title,
        'episodes': self.episodes,
        'status': self.status,
        'target_type': 'Anime'
    }
    if self.target_title_ru is not None:
      basic_json['target_title_ru'] = self.target_title_ru
    if self.target_id is not None:
      basic_json['target_id'] = self.target_id
    if self.score is not None:
      basic_json['score'] = self.score
    return basic_json

  def __repr__(self) -> str:
    return f"Name: {self.target_title}\nTranslated: {self.target_title_ru}\nEpisodes: {self.episodes}\tStatus: {self.status}\tID: {self.target_id}\tScore: {self.score}"

  @staticmethod
  def convertStatus(status):
    if not status:
      return ''
    status = status.lower()
    if status == 'запланировано':
      return 'planned'
    if status == 'смотрю':
      return 'watching'
    if status == 'просмотрено':
      return 'completed'
    if status == 'отложено':
      return 'on_hold'
    if status == 'брошено':
      return 'dropped'
    if status == 'пересматриваю':
      return 'rewatching'
    return status
