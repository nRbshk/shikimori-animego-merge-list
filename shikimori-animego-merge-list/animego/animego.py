from utility.animeItem import AnimeItem
from seleniumWrap import SeleniumWrap
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

wrapper = SeleniumWrap()

ANIMEGO_BASE_URL = 'https://animego.org/anime'


def collectAll(url: str = ANIMEGO_BASE_URL):
  def getContent():
    return wrapper.driver.find_elements(By.XPATH, '//*[@id="anime-list-container"]/div')
  wrapper.driver.get(url)
  items = getContent()
  loaded_items = []
  while (len(items) != len(loaded_items)):
    print(f"Collected: {len(loaded_items)}")
    items = loaded_items
    wrapper.scrollToEnd()
    loaded_items = getContent()

  result = []
  for contentItem in loaded_items:
    title = {
        "target_title_ru": contentItem.find_element(By.XPATH, 'div/div[2]/div[1]/a').text,
        'target_title': contentItem.find_element(By.XPATH, 'div/div[2]/div[2]/div').text
    }
    result.append(AnimeItem(**title))

  return result


def collectByUser(user) -> list[AnimeItem]:
  def getContent():
    return wrapper.driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody').find_elements(By.TAG_NAME, "tr")
  base_url = f'https://animego.org/user/{user}/mylist/anime'
  wrapper.driver.get(base_url)
  items = getContent()
  result = []
  while (len(items) > len(result)):
    print(f"Collected: {len(result)}")
    for i in range(len(result), len(items)):
      content_item = items[i]
      episodes = content_item.find_element(By.XPATH, 'td[5]').text
      title = {"target_title_ru": content_item.find_element(By.XPATH, 'td[2]/a').text,
               "target_title": content_item.find_element(By.XPATH, 'td[2]/div').text,
               "status": content_item.find_element(By.XPATH, 'td[3]/a').get_attribute("data-title"),
               "score": content_item.find_element(By.XPATH, 'td[4]').text,
               "episodes": 0 if episodes == '–' else episodes.split('/')[0].strip()}
      result.append(AnimeItem(**title))
    wrapper.scrollToEnd()
    items = getContent()
  return result
