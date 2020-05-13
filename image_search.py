from .sites import google, bing, yandex, tineye
from .utils.utils import setDriver, dataDict
from billiard import Pool


URL = ""

def search(key):
    with setDriver("res/driver/chromedriver") as driver:
        if key == "google":
            return google.search_google(driver, URL)
        elif key == "bing":
            return bing.search_bing(driver, URL)
        elif key == "yandex":
            return yandex.search_yandex(driver, URL)
        elif key == "tineye":
            return tineye.search_tineye(driver, URL)

def reverse_search(url):
    global URL
    URL = url
    final = ["google", "bing", "yandex", "tineye"]
    pool = Pool(processes = len(final))
    data = pool.map(search, final)
    pool.close()
    return accumulateData(data)

def accumulateData(ol):
    final = dataDict()
    urls = []
    for li in ol:
        for key in ["possible_description", "keywords", "image_text"]:
            if li[key] not in ["", []]:
                final[key] = li[key]
        for x in li["article_links"]:
            if x["url"] not in urls:
                final["article_links"].append(x)
                urls.append(x["url"])
        final["similar_images"] += li["similar_images"]
    return final
