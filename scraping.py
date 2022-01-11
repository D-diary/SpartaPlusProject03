from selenium import webdriver
from bs4 import BeautifulSoup
import time
from selenium.common.exceptions import NoSuchElementException
from pymongo import MongoClient
import requests
from selenium.webdriver.common.by import By

# client = MongoClient('내AWS아이피', 27017, username="아이디", password="비밀번호")
client = MongoClient('localhost', 27017)
db = client.dbsparta_plus_week3

driver = webdriver.Chrome('./chromedriver')

url = "http://matstar.sbs.co.kr/location.html"

driver.get(url)
time.sleep(5)

# # btn_more = driver.find_element_by_css_selector("#foodstar-front-location-curation-more-self > div > button")
# btn_more = driver.find_element(By.CSS_SELECTOR, "#foodstar-front-location-curation-more-self > div > button")
# btn_more.click()
# time.sleep(5)

for i in range(10):
    try:
        btn_more = driver.find_element(By.CSS_SELECTOR,"#foodstar-front-location-curation-more-self > div > button")
        btn_more.click()
        time.sleep(3)
    except NoSuchElementException:
        break

req = driver.page_source
driver.quit()

soup = BeautifulSoup(req, 'html.parser')

#places 에 맛집목록이 저장됨
places = soup.select("ul.restaurant_list > div > div > li > div > a")
print(len(places))

for place in places:
    title = place.select_one("strong.box_module_title").text
    address = place.select_one("div.box_module_cont > div > div > div.mil_inner_spot > span.il_text").text
    category = place.select_one("div.box_module_cont > div > div > div.mil_inner_kind > span.il_text").text
    show, episode = place.select_one("div.box_module_cont > div > div > div.mil_inner_tv > span.il_text").text.rsplit(" ", 1)
    print(title, address, category, show, episode)

    headers = {
        "X-NCP-APIGW-API-KEY-ID": "0a31i2ioet",
        "X-NCP-APIGW-API-KEY": "TkaVYGO9cpbunly7wLdpRDDxyAmIgkPT8uiqOEqx"
    }
    r = requests.get("https://naveropenapi.apigw.ntruss.com/map-geocode/v2/geocode?query={address}", headers=headers)
    response = r.json()
    print(response)

    if response["status"] == "OK":
        if len(response["addresses"]) > 0:
            x = float(response["addresses"][0]["x"])
            y = float(response["addresses"][0]["y"])
            print(title, address, category, show, episode, x, y)
            doc = {
                "title": title,
                "address": address,
                "category": category,
                "show": show,
                "episode": episode,
                "mapx": x,
                "mapy": y
            }
            db.matjips.insert_one(doc)
        else:
            print(title, "좌표를 찾지 못했습니다")
    else:
        print(response["status"])
