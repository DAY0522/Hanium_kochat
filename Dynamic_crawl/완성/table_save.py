import pandas as pd

from crawling import crawling_travel
from openpyxl.utils.exceptions import IllegalCharacterError

from function import make_excel
from function import csv_from_xlsx
from function import xlsx_from_csv

# 서울
seoul_crawling_data = crawling_travel()
seoul_crawling_data.set_component()

start_size = 16
title_size = 2

while start_size < 201:
    seoul_crawling_data.component_initial()

    seoul_crawling_data.crawl_guseok(0, start_size, title_size) # parameter는 지역 index, start_size(크롤링 할 첫 여행지의 index), title_size(크롤링 할 여행지 개수)
    # 다른 지역 검색하려면 () 안에 숫자 바꾸면 됨
    # 서울 0, 인천 1, 대전 2, 대구 3, 광주 4, ...
    # 아래 딕셔너리 인덱스 순서를 기반으로 parameter 설정
    # self.area_dict = {"서울": 1, "인천": 2, "대전": 3, "대구": 4, "광주": 5, "부산": 6, "울산": 7, "세종": 8, "강원": 31, "충북": 32, "충남": 33, "경북": 34, "경남": 35, "전북": 37, "전남": 38, "제주": 39}

    seoul_crawling_data.print_data()

    seoul_crawling_data.make_matrix() # 데이터 생성
    seoul_df = pd.DataFrame(seoul_crawling_data.raw_data)
    make_excel(seoul_df, "sample")

    start_size += title_size
