from utility import AnimeItem
from seleniumWrap import SeleniumWrap
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement

wrapper = SeleniumWrap()


def getListContents():
  return wrapper.driver.find_element(By.XPATH, '//*[@id="content"]/table/tbody').find_elements(By.TAG_NAME, "tr")


def parseListContent(contentElements: list[WebElement]) -> list[AnimeItem]:
  data = []
  for cont in contentElements:
    russianName = cont.find_element(By.XPATH, 'td[2]/a').text
    name = cont.find_element(By.XPATH, 'td[2]/div').text
    status = cont.find_element(By.XPATH, 'td[3]/a').get_attribute("data-title")
    episodes = cont.find_element(By.XPATH, 'td[5]').text
    data.append(AnimeItem(name, russianName, episodes, None, status))
  return data


def receiveItems(user) -> list[AnimeItem]:
  user = "siel_die"
  base_url = f'https://animego.org/user/{user}/mylist/anime'
  wrapper.driver.get(base_url)
  items = getListContents()
  loaded_items = []
  while (len(items) != len(loaded_items)):
    items = loaded_items
    wrapper.scrollToEnd()
    loaded_items = getListContents()

  return parseListContent(loaded_items)
  
