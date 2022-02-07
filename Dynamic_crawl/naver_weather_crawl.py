import selenium
from selenium import webdriver
from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options

from random import *

options = Options()

# chrome을 전체화면으로 넓히는 옵션입니다.
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')

# executable_path에는 chromedriver 실행 파일의 경로를 넣고, chrome_options에는 options 변수를 넣습니다.
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)

# 장소 검색
place = input("날씨 검색할 여행지를 입력하세요.")
URL = 'https://search.naver.com/search.naver?ie=UTF-8&sm=whl_hty&query=' + str(place)
driver.get(url=URL)

# 장소 날씨 검색
location = driver.find_element_by_css_selector("#place_main_ct > div > div > div > div.ct_box_area > div.bizinfo_area > div > div:nth-child(2) > div > ul > li:nth-child(1) > span > a > span.txt")  # Copy selector
URL = 'https://search.naver.com/search.naver?ie=UTF-8&sm=whl_hty&query=' + location.text + ' 날씨'
driver.get(url=URL)