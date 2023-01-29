from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from time import sleep


class SeleniumWrap:
  def __init__(self):
    self.driver = self.__createWebdriver()

  def scrollToEnd(self):
    self.driver.execute_script("window.scrollTo(window.scrollY, document.body.scrollHeight);")
    sleep(0.7)

  def __setupChromeOptions(self):
    chrome_options = Options()
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("window-size=1920,1080")
    chrome_options.add_argument('--disable-dev-shm-usage')
    return chrome_options

  def __createWebdriver(self):
    return webdriver.Chrome(options=self.__setupChromeOptions())
