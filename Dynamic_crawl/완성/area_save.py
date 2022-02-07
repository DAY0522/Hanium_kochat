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
from time import sleep

from random import *

options = Options()

# chrome을 전체화면으로 넓히는 옵션입니다.
options = webdriver.ChromeOptions()
options.add_argument('window-size=1920,1080')

# executable_path에는 chromedriver 실행 파일의 경로를 넣고, chrome_options에는 options 변수를 넣습니다.
driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
driver.implicitly_wait(1)

# chromedriver.exe의 파일명을 넣어주면 된다. (확장자 없이)
# 만약 chromedriver.exe가 다른 곳에 있다면 절대경로로 넣어주면 된다.

# 입력한 지역탭으로 이동
area_dict = {"서울" : 1, "인천" : 2, "대전" : 3, "대구" : 4, "광주" : 5, "부산" : 6, "울산" : 7, "세종" : 8,
             "강원" : 31, "충북" : 32, "충남" : 33, "경북" : 34, "경남" : 35, "전북" : 37, "전남" : 38, "재주" : 39,}
area = [] # 딕셔너리에서 지역명만 list에 저장
area_id = [] # 딕셔너리에서 id만 list에 저장
area_url = [] # 각 지역의 url을 list에 저장

for key in area_dict.keys():
    area.append(key)
    area_id.append(area_dict[key])

area_travel_destination = [] # 여행지 저장(모든 지역에 대한 여행지)
title_size = 15 # 각 지역별 출력할 여행지 개수

for num in range(len(area_id)):
    travel_destination = [] # 여행지 저장(특정 지역에 대한 여행지)
    area_url.append("https://korean.visitkorea.or.kr/list/ms_list.do?areacode=" + str(area_id[num]))
    driver.implicitly_wait(1)

    driver.get(url=area_url[num])  # 입력된 url 창을 크롬으로 켬

    # 인기순으로 정렬
    pop_sort_box = driver.find_element_by_xpath('// div [@ class = \'btn_txt\']//*[@id="3"]')  # Copy Xpath
    pop_sort_box.click()
    sleep(5)

    # 여행지 카테고리 클릭(전체로 되면 여행기사도 포함이 돼 우리가 원하는 여행지 타이틀만을 가져올 수 없기 때문)
    pop_sort_box = driver.find_element_by_xpath('//*[@id="Tour"]/button/span')  # Copy Xpath
    pop_sort_box.click()
    sleep(3)

    # 200개의 여행지를 불러옴
    for i in range(1, title_size + 1):
        page = int((i - 1) / 10 + 1)  # 현재 페이지 번호
        title_num = int(((i - 1) % 10) + 1)  # 해당 title text의 인덱스

        # 여행지 제목 출력
        title = driver.find_element_by_css_selector(
            "#contents > div.wrap_contView.clfix > div.box_leftType1 > ul > li:nth-child(" + str(
                title_num) + ") > div.area_txt > div > a")  # Copy selector
        travel_destination.append(title.text)  # list에 여행지 이름 저장

        # 해당 페이지의 모든 title을 출력하면 다음 페이지로 넘어감
        if title_num == 10:
            page_box = driver.find_element_by_xpath(
                '// div [@ class = \'page_box\']//*[@id=\"' + str(page + 1) + '\"]')  # 다음 페이지 클릭
            page_box.click()
            sleep(3)

        if i == title_size:
            area_travel_destination.append(travel_destination)

# 제대로 코드 작성됐나 출력해봄
for num in range(len(area_dict)):
    print(area[num] + " 여행지 추천 ! ! !")
    print(area_travel_destination[num])
    print("\n")