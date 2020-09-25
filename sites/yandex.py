from selenium.common.exceptions import TimeoutException,InvalidArgumentException
from selenium.webdriver.support import expected_conditions as EC
from ..utils.utils import efficientGet, linkDict, dataDict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..conf import TIMEOUT
from time import sleep
import validators

YANDEX_URL = "https://www.yandex.com/images/"

def search_yandex(driver, url):
    efficientGet(driver, YANDEX_URL)
    wait = WebDriverWait(driver, TIMEOUT)
    results = dataDict()
    try:
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//button[@aria-label='Image search']")))
        driver.execute_script("arguments[0].click();", element)
    except TimeoutException:
        return results
    if validators.url(url):
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='cbir-url']")))
            element.send_keys(url)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//button[@name='cbir-submit']")))
            driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            return results
    else:
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='upfile']")))
            element.send_keys(url)
        except TimeoutException:
            pass
        except InvalidArgumentException:
            print("Wrong file path specified")
            return results
    try:
        element = wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(@class, "cbir-page-content")]')))
        sleep(2)
        text = element.get_attribute("innerHTML")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            a = soup.find("div", {'class': "Tags Tags_type_simple"})
            if a:
                for b in a.find_all("a"):
                    results["keywords"].append(b.text)
            links = []
            for a in soup.find_all("div", {"class": "other-sites__snippet-title"}):
                link = linkDict()
                a = a.find("a")
                if a:
                    link["url"] = a.get("href", "")
                    link["title"] = a.text
                links.append(link)
            results["article_links"] = links
            for a in soup.find_all("img", {'class': "cbir-similar__image"}):
                results["similar_images"].append("https:" + a.get("src") if a.get("src") else "")
    except TimeoutException:
        pass
    return results
