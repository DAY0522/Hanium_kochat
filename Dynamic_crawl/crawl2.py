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
from prea import has_xpath

class crawling_travel:
    def __init__(self):
        self.area_dict = {"서울": 1, "인천": 2, "대전": 3, "대구": 4, "광주": 5, "부산": 6, "울산": 7, "세종": 8,
                     "강원": 31, "충북": 32, "충남": 33, "경북": 34, "경남": 35, "전북": 37, "전남": 38, "제주": 39 }
        self.area = []  # 딕셔너리에서 지역명만 list에 저장
        self.area_id = []  # 딕셔너리에서 id만 list에 저장
        self.area_url = []  # 각 지역의 url을 list에 저장

        # DB table 변수
        self.member_id = [] # 일련번호
        self.member_title = [] # 여행지명
        self.member_area = [] # 지역명
        self.member_sub_area = [] # 세부지역명
        self.member_address = [] # 주소
        self.member_coordinate = [] # 좌표(주소좌표화)
        self.member_tel = [] # 전화번호
        self.member_explain = [] # 여행지 설명
        self.member_image = [] # 사진

        self.xpath_address = "//*[@id=\"detailinfoview\"]/div/div[1]/div/ul/li[2]/span"
        self.xpath_tel = "/html/body/div[3]/div[2]/div[4]/div[4]/div/div[1]/div/ul/li[1]/span[2]"
        self.xpath_explain = "//*[@id=\"detailGo\"]/div[2]/div/div[1]/div/p"
        self.xpath_image = ""

    def crawl_guseok(self):
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

        for key in self.area_dict.keys():
            self.area.append(key)
            self.area_id.append(self.area_dict[key])

        title_size = 2  # 각 지역별 출력할 여행지 개수

        for num in range(len(self.area_dict)):
            # 지역별 url에 들어가기
            self.area_url.append("https://korean.visitkorea.or.kr/list/ms_list.do?areacode=" + str(self.area_id[num]))
            driver.implicitly_wait(1)

            # title_size개의 여행지를 불러옴
            for i in range(1, title_size + 1):
                page = int((i - 1) / 10 + 1)  # 현재 페이지 번호
                page_next = int(((i / 10) - 1) / 5)  # 현재 페이지로 가기 위해 다음 페이지 버튼 누르는 횟수
                title_num = int(((i - 1) % 10) + 1)  # 해당 title text의 인덱스

                driver.get(url=self.area_url[num])  # 입력된 url 창을 크롬으로 켬
                sleep(2)

                # 인기순으로 정렬
                pop_sort_box = driver.find_element_by_xpath('//div [@ class = \'btn_txt\']//*[@id="3"]')  # Copy Xpath
                pop_sort_box.send_keys(Keys.ENTER)
                sleep(5)

                # 여행지 카테고리 클릭(전체로 되면 여행기사도 포함이 돼 우리가 원하는 여행지 타이틀만을 가져올 수 없기 때문)
                pop_sort_box = driver.find_element_by_xpath('//*[@id="Tour"]/button/span')  # Copy Xpath
                pop_sort_box.click()
                sleep(3)

                # 다음 페이지 버튼 누르기
                for n in range(page_next):
                    next_page_box = driver.find_element_by_xpath('//*[@id=\"' + str(n * 5 + 1) + '\"]')  # Copy Xpath
                    next_page_box.click()
                    sleep(3)

                # 해당 페이지 누르기
                page_box = driver.find_element_by_xpath(
                    '// div [@ class = \'page_box\']//*[@id=\"' + str(page) + '\"]')  # Copy Xpath
                page_box.click()
                sleep(4)

                # 일련번호 추가
                self.member_id.append(num * title_size + i)


                # 여행지명 추가
                title = driver.find_element_by_css_selector(
                    "#contents > div.wrap_contView.clfix > div.box_leftType1 > ul > li:nth-child(" + str(
                        title_num) + ") > div.area_txt > div > a")  # Copy selector
                self.member_title.append(title.text)


                # 여행지 지역명 추가
                self.member_area.append(self.area[num])

                # 상세정보 출력을 위해 해당 여행지 페이지로 들어감
                place_box = driver.find_element_by_xpath(
                    '//*[@id="contents"]/div[2]/div[1]/ul/li[' + str(title_num) + ']/div[2]/div/a')  # Copy Xpath
                place_box.send_keys(Keys.ENTER)
                sleep(1)

                print(has_xpath(self.xpath_address))
                print(has_xpath("/html/body/div[3]/div[2]/div[4]/div[4]/div/div[1]/div/ul/li[1]/span[2]"))

                print(has_xpath("/html/body/div[3]/div[2]/div[4]/div[4]/div/div[1]/div/ul/li[1]/span[2]"))

                try:
                    driver.find_element_by_xpath("/html/body/div[3]/div[2]/div[4]/div[4]/div/div[1]/div/ul/li[1]/span[2]")
                    print("True")
                except:
                    print("False")