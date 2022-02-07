# 각 지역별 여행지 출력하는 코드
# 여행지의 개수를 변경하고 싶으면 title_size 변수의 할당하는 값을 바꾸면 됨
# (title_size는 for문이 돌아가는 범위에 쓰임)

import selenium
from selenium import webdriver

from selenium.webdriver import ActionChains

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

from time import sleep

import pandas as pd     # pip install pands필요
import numpy as np
import os

from bs4 import BeautifulSoup

# xpath 존재 유무 확인
def has_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

def has_selector(driver, selector):
    try:
        driver.find_element_by_css_selector(selector)
        return True
    except:
        return False

def has_id(driver, id):
    try:
        driver.find_element_by_id(id)
        return True
    except:
        return False

options = Options()

# chrome을 전체화면으로 넓히는 옵션
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')

# executable_path에는 chromedriver 실행 파일의 경로를 넣고, chrome_options에는 options 변수를 넣습니다.
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
driver.implicitly_wait(1)

# chromedriver.exe의 파일명을 넣어주면 된다. (확장자 없이)
# 만약 chromedriver.exe가 다른 곳에 있다면 절대경로로 넣어주면 된다.

URL = "https://korean.visitkorea.or.kr/detail/ms_detail.do?cotid=7e32193a-70c6-47a8-aae4-0015a79d121f&big_category=A02&mid_category=A0206&big_area=1"
driver.get(url=URL)  # 입력된 url 창을 크롬으로 켬

# 주소 출력
Address_index_2 = driver.find_element_by_css_selector("#detailinfoview > div > div.inr_wrap > div > ul > li:nth-child(2) > strong").text
Address_index_3 = driver.find_element_by_css_selector("#detailinfoview > div > div.inr_wrap > div > ul > li:nth-child(3) > strong").text

if Address_index_2 == "주소":
    member_address.append(Address_index_2.text)
elif Address_index_3 == "주소":
    member_address.append(Address_index_3.text)
else:
    member_address.append("\0")


