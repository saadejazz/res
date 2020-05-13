from selenium.common.exceptions import TimeoutException,InvalidArgumentException
from ..utils.utils import efficientGet, dataDict, linkDict, downloadMedia
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from ..utils.dat import DATA_DICT, LINK_DICT
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..conf import TIMEOUT
from time import sleep
import validators
import os

BING_URL = "https://www.bing.com/?scope=images&nr=1&FORM=NOFORM"

def search_bing(driver, url):
    efficientGet(driver, BING_URL)
    wait = WebDriverWait(driver, TIMEOUT)
    results = dataDict()
    remove = False
    try:
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Search using an image']")))
        driver.execute_script("arguments[0].click();", element)
    except TimeoutException:
        return results
    if validators.url(url):
        remove = True
        try:
            try:
                os.makedirs("temp/")
            except FileExistsError:
                pass
            ext = url.split(".")[-1]
            downloadMedia(url, f'temp/bing.{ext}')
            url = os.getcwd() + f'/temp/bing.{ext}'
        except Exception as e:
            print("Failed to download media", e)
            return results
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='sb_fileinput']")))
        element.send_keys(url)
    except TimeoutException:
        pass
    except InvalidArgumentException:
        print("Wrong file path specified")
        return results
    try:
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="detailCanvas"]')))
        sleep(2)
        text = element.get_attribute("innerHTML")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            a = soup.find("div", id = "text_container")
            if a:
                results["image_text"] = a.text
            links = []
            for a in soup.find_all("div", {"class": "pigc"}):
                link = linkDict()
                a = a.find("div", {'class': 'pilvi'})
                if a:
                    a = a.find("a")
                    if a:
                        link["url"] = a.get("href", "")
                        link["title"] = a.text
                links.append(link)
            results["article_links"] = links
            a = soup.find("div", id = "i_results")
            if a:
                for b in a.find_all("img", {'alt': "See related image detail"}):
                    results["similar_images"].append(b.get("src", ""))
    except TimeoutException:
        pass
    if remove:
        try:
            os.remove(url)
        except FileNotFoundError:
            pass
    return results
