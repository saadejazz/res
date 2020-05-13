from selenium.common.exceptions import TimeoutException,InvalidArgumentException
from selenium.webdriver.support import expected_conditions as EC
from ..utils.utils import efficientGet, dataDict, linkDict
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
from ..conf import TIMEOUT
from time import sleep
import validators

GOOGLE_URL = "https://images.google.com/?gws_rd=ssl"

def search_google(driver, url):
    efficientGet(driver, GOOGLE_URL)
    wait = WebDriverWait(driver, TIMEOUT)
    results = dataDict()
    try:
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@aria-label='Search by image']")))
        driver.execute_script("arguments[0].click();", element)
    except TimeoutException:
        return results
    if validators.url(url):
        try:
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='image_url']")))
            element.send_keys(url)
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@value='Search by image']")))
            driver.execute_script("arguments[0].click();", element)
        except TimeoutException:
            return results
    else:
        try:
            element = wait.until(EC.visibility_of_element_located((By.XPATH, "//a[text()='Upload an image']")))
            driver.execute_script("arguments[0].click();", element)
            element = wait.until(EC.presence_of_element_located((By.XPATH, "//input[@name='encoded_image']")))
            element.send_keys(url)
        except TimeoutException:
            return results
        except InvalidArgumentException:
            print("Wrong file path specified")
            return results
    try:
        element = wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@id='res']")))
        sleep(2)
        text = element.get_attribute("innerHTML")
        if text:
            soup = BeautifulSoup(text, "html.parser")
            a = soup.find("div", id = "topstuff")
            if a:
                a = a.find("div", {'class': 'card-section'})
                if a:
                    a = a.find(lambda tag: tag.name == "div" and "Possible related search" in tag.text)
                    if a:
                        a = a.find('a')
                        if a:
                            results["possible_description"] = a.text
            a = soup.find("div", id = "search")
            if a:
                links = []
                for s in a.find_all("div", {'class': 'r'}):
                    g = s.find('a')
                    link = linkDict()
                    link["url"] = g.get("href", "")
                    link["title"] = g.text.partition(" ...")[0]
                    links.append(link)
                results["article_links"] = links
            for img in soup.find_all("img", {'alt': "Image result"}):
                results["similar_images"].append(img.get("src", ""))
    except TimeoutException:
        return results
    return results
