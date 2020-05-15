from selenium.common.exceptions import TimeoutException, JavascriptException, NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from selenium import webdriver
from bs4 import BeautifulSoup
from time import sleep

def setDriver(executable_path, headless = False, maximize = True):
    chrome_options = webdriver.ChromeOptions()
    prefs = {"profile.default_content_setting_values.notifications" : 2}
    chrome_options.add_experimental_option("prefs",prefs)
    if maximize:
        chrome_options.add_argument("--start-maximized")
    if headless:
        chrome_options.add_argument("--headless")
    return webdriver.Chrome(executable_path = executable_path, chrome_options=chrome_options)

def efficientGet(driver, url):
    if driver.current_url != url:
        driver.get(url)

def downloadMedia(mediaDirectory, localDirectory):
    with open(localDirectory, "wb") as filex:
        filex.write(urlopen(mediaDirectory).read())
        filex.close()

def dataDict():
    return {
        "possible_description": "",
        "keywords": [],
        "image_text": "",
        "similar_images": [],
        "article_links": []
    }

def linkDict():
    return {
        "title": "",
        "url": ""
    }
