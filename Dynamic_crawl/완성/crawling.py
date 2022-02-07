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

from bs4 import BeautifulSoup
from time import sleep
from function import has_xpath
from function import has_selector
from function import has_id


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
        self.member_category = [] # 여행지 설명
        self.member_image = [] # 사진

        self.xpath_area = "/html/body/div[3]/div[1]/div[2]/span"
        self.selector_tel = "#detailinfoview > div > div.inr_wrap > div > ul > li:nth-child(1) > span.pc"
        self.xpath_explain = "//*[@id=\"detailGo\"]/div[2]/div/div[1]/div/p"
        self.xpath_image = "/html/body/div[3]/div[2]/div[3]/div[2]/div[1]/div[1]/div[1]/a"
        self.xpath_image_after_click = "/html/body/div[4]/div[1]/div[1]/div/div[1]/div/div[1]/div[1]/div/img"
        self.xpath_category_add_but = "/html/body/div[3]/div[2]/div[4]/div[9]/button"

        self.all_subarea = []  # 학습시키기 위해 subarea 추출하기 위한 list
        self.raw_data = {}

    def component_initial(self):
        self.member_id = [] # 일련번호
        self.member_title = [] # 여행지명
        self.member_area = [] # 지역명
        self.member_sub_area = [] # 세부지역명
        self.member_address = [] # 주소
        self.member_coordinate = [] # 좌표(주소좌표화)
        self.member_tel = [] # 전화번호
        self.member_explain = [] # 여행지 설명
        self.member_category = [] # 여행지 설명
        self.member_image = [] # 사진

    def set_component(self): # class 멤버들의 기본값을 설정하는 함수
        for key in self.area_dict.keys():
            self.area.append(key)
            self.area_id.append(self.area_dict[key])

        for num in range(len(self.area_dict)):
            # 지역별 url list에 저장하기
            self.area_url.append("https://korean.visitkorea.or.kr/list/ms_list.do?areacode=" + str(self.area_id[num]))


    def crawl_guseok(self, num, start_size, title_size): # 지역별 crawling 하는 함수
        options = Options()

        # chrome을 전체화면으로 넓히는 옵션
        options = webdriver.ChromeOptions()
        options.add_argument('window-size=1920,1080')

        # executable_path에는 chromedriver 실행 파일의 경로를 넣고, chrome_options에는 options 변수를 넣습니다.
        driver = webdriver.Chrome(executable_path='./chromedriver', options=options)
        driver.implicitly_wait(1)

        # chromedriver.exe의 파일명을 넣어주면 된다. (확장자 없이)
        # 만약 chromedriver.exe가 다른 곳에 있다면 절대경로로 넣어주면 된다.


        each_subarea = [] # 각 지역별 상세지역 저장할 list

        # title_size개의 여행지를 불러옴
        for i in range(start_size, title_size + start_size):
            print(self.area[num], i)
            page = int((i - 1) / 10 + 1)  # 현재 페이지 번호
            page_next = int(((i / 10) - 1) / 5)  # 현재 페이지로 가기 위해 다음 페이지 버튼 누르는 횟수
            title_num = int(((i - 1) % 10) + 1)  # 해당 title text의 인덱스

            driver.get(url=self.area_url[num])  # 입력된 url 창을 크롬으로 켬
            sleep(3)

            # 인기순으로 정렬
            pop_sort_box = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[1]/div[1]/div/button[3]')  # Copy Xpath
            pop_sort_box.send_keys(Keys.ENTER)
            sleep(5)

            # 여행지 카테고리 클릭(전체로 되면 여행기사도 포함이 돼 우리가 원하는 여행지 타이틀만을 가져올 수 없기 때문)
            Tour_sort_box = driver.find_element_by_xpath('/html/body/div[2]/div[2]/div[2]/div[2]/ul[1]/li[2]/button/span')  # Copy Xpath
            Tour_sort_box.click()
            sleep(3)

            # 다음 페이지 버튼 누르기
            for n in range(1, page_next + 1):
                next_page_box = driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[1]/div[2]/a[' + str(n * 5 + 1) + ']') # Copy Xpath
                next_page_box.send_keys(Keys.ENTER)
                sleep(3)


            # 해당 페이지 누르기
            page_box = driver.find_element_by_xpath(
                '/html/body/div[2]/div[2]/div[1]/div[2]/a[' + str(page) + ']') # Copy Xpath
            page_box.send_keys(Keys.ENTER)
            sleep(4)


            # 일련번호 추가
            self.member_id.append(num * title_size + i - 1)


            # 상세정보 출력을 위해 해당 여행지 페이지로 들어감
            place_box = driver.find_element_by_xpath(
                '//*[@id="contents"]/div[2]/div[1]/ul/li[' + str(title_num) + ']/div[2]/div/a')  # Copy Xpath
            place_box.send_keys(Keys.ENTER)
            sleep(3)


            # 여행지명 추가
            title = driver.find_element_by_xpath("/ html / body / div[3] / div[1] / h2")  # Copy Xpath
            self.member_title.append(title.text)


            # 지역 및 상세지역 출력
            if has_xpath(driver, self.xpath_area) == True:
                area_full = driver.find_element_by_xpath(self.xpath_area)  # Copy Xpath
                area_full_text = area_full.text.split(' ') # 지역 / 상세지역 구분

                self.member_area.append(area_full_text[0]) # 지역을 list에 추가

                if len(area_full_text) == 1: # 여행지에 따라서 상세지역이 존재하지 않는 경우가 존재하므로 확인
                    self.member_sub_area.append("\0")
                else :
                    self.member_sub_area.append(area_full_text[1])
                    each_subarea.append(area_full_text[1])

            else:
                self.member_area.append("\0")
                self.member_sub_area.append("\0")


            # 주소 출력
            if str(driver.find_element_by_css_selector("#detailinfoview > div > div.inr_wrap > div > ul > li:nth-child(2) > strong").text) == "주소":
                Address = driver.find_element_by_css_selector("#detailinfoview > div > div.inr_wrap > div > ul > li:nth-child(2) > span")
                self.member_address.append(Address.text)
            elif str(driver.find_element_by_css_selector("#detailinfoview > div > div.inr_wrap > div > ul > li:nth-child(3) > strong").text) == "주소":
                Address = driver.find_element_by_css_selector("#detailinfoview > div > div.inr_wrap > div > ul > li:nth-child(3) > span")
                self.member_address.append(Address.text)
            else:
                self.member_address.append("\0")


            # 좌표 추가
            self.member_coordinate.append("\0")

            # 전화번호 추가
            if has_selector(driver, self.selector_tel) == True:
                tel = driver.find_element_by_css_selector(self.selector_tel)  # Copy Xpath
                self.member_tel.append(tel.text)
            else:
                self.member_tel.append("\0")


            # 여행지 설명 추가
            if has_xpath(driver, self.xpath_explain) == True:
                title_explain = driver.find_element_by_xpath(self.xpath_explain)  # Copy Xpath
                self.member_explain.append(title_explain.text)
            else:
                self.member_explain.append("\0")


            # 카테고리 추가
            if has_id(driver, "btn_more") == True:
                add_but = driver.find_element_by_id("btn_more").click()
                sleep(2)

            index = 1
            category_str = []

            while has_selector(driver, "#detailGo > div.tag_cont > div > ul > li:nth-child(" + str(index) + ") > a > span") == True:
                category = driver.find_element_by_css_selector(
                    "#detailGo > div.tag_cont > div > ul > li:nth-child(" + str(index) + ") > a > span")  # Copy Xpath
                category_str.append(category.text)
                index = index + 1

            self.member_category.append(category_str)


            # 사진 추가
            # ※카테고리 이전에 함수 실행하면 add_but이 없기 때문에 error 발생함 꼭 카테고리 추가 이후에 사진 추가 해야함!※
            while has_xpath(driver, self.xpath_image_after_click) == False:
                if has_xpath(driver, self.xpath_image) == True:
                    image = driver.find_element_by_xpath(self.xpath_image)  # Copy Xpath
                    image.send_keys(Keys.ENTER)
                else:
                    break
                sleep(1)

            req = driver.page_source
            soup = BeautifulSoup(req, 'html.parser')

            if has_xpath(driver, self.xpath_image_after_click) == True:
                img_thumnails = soup.select_one('#img0')  # Copy Xpath
                self.member_image.append(img_thumnails['src'])
            else:
                self.member_image.append('\0')

        self.all_subarea.append(tuple(each_subarea))
        driver.close()

    def print_data(self):
        print(self.all_subarea)
        print('\n')
        print(self.member_id)
        print("\n")
        print(self.member_title)
        print("\n")
        print(self.member_area)
        print("\n")
        print(self.member_sub_area)
        print("\n")
        print(self.member_tel)
        print("\n")
        print(self.member_explain)
        print("\n")
        print(self.member_address)
        print("\n")
        print(self.member_coordinate)
        print("\n")
        print(self.member_image)
        print("\n")
        print(self.member_category)
        print("\n")

    def make_matrix(self):
        # 각 열의 순서는
        # 일련번호, 여행지명, 지역명, 세부지역명, 주소, 좌표, 전화번호, 여행지설명, 카테고리, 사진 순서
        self.raw_data = {'id' : self.member_id,
                        'title': self.member_title,
                        'area': self.member_area,
                        'sub area': self.member_sub_area,
                        'address': self.member_address,
                        'coordinate': self.member_coordinate,
                        'tel': self.member_tel,
                        'explain': self.member_explain,
                        'image': self.member_image,
                        'category': self.member_category
                        }  # 리스트 자료형으로 생성