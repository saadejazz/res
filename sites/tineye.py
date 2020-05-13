from selenium.common.exceptions import TimeoutException,InvalidArgumentException
from selenium.webdriver.support import expected_conditions as EC
from ..utils.utils import efficientGet, dataDict, linkDict
from selenium.webdriver.support.ui import WebDriverWait
from ..utils.dat import DATA_DICT, LINK_DICT
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..conf import TIMEOUT
from time import sleep
import validators

TINEYE_URL = "https://tineye.com/"

def search_tineye(driver, url):
    efficientGet(driver, TINEYE_URL)
    wait = WebDriverWait(driver, TIMEOUT)
    results = dataDict()
    if validators.url(url):
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='url_box']")))
        element.send_keys(url)
        element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='url_submit']")))
        driver.execute_script("arguments[0].click();", element)
    else:
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@id='upload_box']")))
            element.send_keys(url)
        except TimeoutException:
            pass
        except InvalidArgumentException:
            print("Wrong file path specified")
            return results
    try:
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[@id="match-summary"]')))
        sleep(2)
        text = element.get_attribute("innerHTML")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            links = []
            for a in soup.find_all("div", {"class": "match"}):
                link = linkDict()
                a = a.find("a")
                if a:
                    link["url"] = a.get("href", "")
                    link["title"] = a.text
                links.append(link)
            results["article_links"] = links
    except TimeoutException:
        pass
    return results
