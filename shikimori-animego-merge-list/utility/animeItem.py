class AnimeItem:
  def __init__(self, original: str, translated: str, episodes: str, id: str | None, status: str | None):
    self.original = original
    self.translated = translated
    self.episodes = episodes
    self.id = id
    self.status = status

  def asJSON(self) -> dict[str, str]:
    basic = {'original': self.original, 'translated': self.translated, 'episodes': self.episodes}
    if self.id is not None:
      basic['id'] = self.id
    if self.status is not None:
      basic['status'] = self.status
    return basic
  
  def __repr__(self) -> str:
    return f"Name: {self.original}\nTranslated: {self.translated}\nEpisodes: {self.episodes}\tStatus: {self.status}\tID: {self.id}\n"
