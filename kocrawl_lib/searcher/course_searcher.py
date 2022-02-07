"""
@auther Hyunwoong
@since {6/21/2020}
@see : https://github.com/gusdnd852
"""

from random import randint
from kocrawl.searcher.base_searcher import BaseSearcher

import pymysql
import random
import json
import itertools
import pandas as pd
import requests
from tqdm import tqdm
import numpy as np
from haversine import haversine
from itertools import permutations

# DB 접속
connect = pymysql.connect(host='haniumdb1.cclzfuhgqdpp.ap-northeast-2.rds.amazonaws.com', user='admin', password='kkklp1720', db='hanium', charset='utf8')
cur = connect.cursor(pymysql.cursors.DictCursor)

class CourseSearcher(BaseSearcher):

    def __init__(self):
        self.data_dict_1 = {
            # 데이터를 담을 딕셔너리 구조를 정의합니다.
            'idx': [], 'name': [],
            'tel': [], 'context': [],
            'category': [], 'address': [],
            'thumUrl': [], 'theme' : []
            # sort_num은 경로 순서
        }

        self.data_dict_2 = {
            # 데이터를 담을 딕셔너리 구조를 정의합니다.
            'idx': [], 'name': [],
            'tel': [], 'context': [],
            'category': [], 'address': [],
            'thumUrl': [], 'theme' : []
        }

        self.data_dict_3 = {
            # 데이터를 담을 딕셔너리 구조를 정의합니다.
            'idx': [], 'name': [],
            'tel': [], 'context': [],
            'category': [], 'address': [],
            'thumUrl': [], 'theme' : []
        }

        self.data_dict_4 = {
            # 데이터를 담을 딕셔너리 구조를 정의합니다.
            'idx': [], 'name': [],
            'tel': [], 'context': [],
            'category': [], 'address': [],
            'thumUrl': [], 'theme' : []
        }

        self.sorted_data = []

        self.data_course = {
            # 데이터를 담을 딕셔너리 구조를 정의합니다.
            'sequence': [], 'distance': [],
            'sum_distance' : []
        }

        self.COURSE_SIZE = 4
        self.index = np.arange(self.COURSE_SIZE)

        self.test_data = pd.DataFrame([])

        self.url = 'http://api.vworld.kr/req/address?'
        self.params = 'service=address&request=getcoord&version=2.0&crs=epsg:4326&refine=true&simple=false&format=json&type='
        self.road_type = 'road'
        self.address = '&address='
        self.keys = '&key='
        self.primary_key = 'F7F5CAB1-F890-3249-A529-89AD97FA8D4B'

    def _make_area(self, location: str) -> str:
        """
        데이터를 출력하기 위해 query 들어가야 할 지역명을 구분
        (1. area, 2. area + sub_area, 3. sub_area 세 가지 방식으로 구분해야 함)

        :param location: kochat이 인식한 지역
        :return: (area, sub_area) 형태의 튜플
        """
        location_list = location.split(' ')
        if len(location_list) >= 2:
            area = location_list[0]
            sub_area = location_list[1]
        elif self.disting_area(location) == 1:  # sub_area로 들어온 경우
            area = 0
            sub_area = location_list[0]
        elif self.disting_area(location) == 0:  # area로 들어온 경우
            area = location_list[0]
            sub_area = 0
        return (area, sub_area)

    def disting_area(self, sub_area: str) -> str:
        """
        sub_area인지 구분하는 함수

        :param sub_area:
        :return: 0 or 1
        str에 시, 군, 구가 있으면 즉 sub_area면 1을 return
                         없으면 즉     area면 0을 returb
        """
        if sub_area.find('시') != -1:
            return 1
        elif sub_area.find('군') != -1:
            return 1
        elif sub_area.find('구') != -1 and sub_area != "대구":
            return 1
        return 0

    def _make_query(self, location: str, theme: str):
        """
        검색할 쿼리를 만듭니다.
        :param location: 지역
        :param theme: 테마
        :return: "지역 장소"로 만들어진 쿼리
        """
        if self._make_THEME_query(theme) != 0:  # theme이 존재하는 경우
            if self._make_area(location)[1] == 0:  # area만 입력된 경우
                query = 'SELECT * from information WHERE area=%s and category LIKE %s'
                cur.execute(query, (location, ("%" + theme + "%",)))
            elif self._make_area(location)[0] == 0:  # sub_area만 입력된 경우
                query = "SELECT * from information WHERE sub_area=%s and category LIKE %s"
                cur.execute(query, (location, ("%" + theme + "%",)))
            else:
                query = "SELECT * from information WHERE area=%s and sub_area=%s and category LIKE %s"
                cur.execute(query, (self._make_area(location)[0], self._make_area(location)[1], ("%" + theme + "%",)))

        else:  # theme가 존재하지 않는 경우
            if self._make_area(location)[1] == 0:  # area만 입력된 경우
                query = "SELECT * from information WHERE area=%s"
                cur.execute(query, self._make_area(location)[0])
            elif self._make_area(location)[0] == 0:  # sub_area만 입력된 경우
                query = "SELECT * from information WHERE sub_area=%s"
                cur.execute(query, self._make_area(location)[1])
            else:
                query = "SELECT * from information WHERE area=%s and sub_area=%s"
                cur.execute(query, self._make_area(location)[0], self._make_area(location)[1])

        connect.commit()

        rows = cur.fetchall()  # query에 해당하는 모든 열 불러오기
        return rows

    def _make_THEME_query(self, theme: str) -> str:
        """
        category가 있는 경우 query문 뒷 부분 추가할 내용을 return하는 함수
        :param theme: 테마
        :return: 0인 경우 theme 존재 X
                 0이 아닌 경우 theme 존재
        """
        if theme != "관광지":
            THEME_query = "and category LIKE \'%" + theme + "%\'"
        else:
            THEME_query = 0
        return THEME_query

    def edit_category(self, data_category: str) -> list:
        """
        DB에 저장된 category(str)을 list 형태로 수정하는 함수

        :param data_category: DB에 저장된 카테고리 str
        :return: 카테고리 list
        """
        category_list = data_category.split('\', \'')
        category_list[0] = category_list[0][2:]
        category_list[len(category_list) - 1] = category_list[len(category_list) - 1][:-2]

        return category_list

    def select_travel(self, len):
        """
        여행지를 random으로 선택하기 위해
        중복 없이 index 4개를 반환해주는 함수
        :param len: 최대 index 크기(query문에 적합한 여행지의 개수와 동일)
        :return: index 4개를 가진 list
        """
        nList = set()

        for x in range(self.COURSE_SIZE):
            n = random.randint(0, len - 1)
            while n in nList:
                n = random.randint(0, len - 1)
            nList.add(n)
        return list(nList)

    # 이 아래는 경로 탐색 시 필요한 코드들
    def request_geo(self, road):
        page = requests.get(
            self.url + self.params + self.road_type + self.address + road + self.keys + self.primary_key)
        json_data = page.json()
        return json_data

    def extraction_geo(self, test_data):
        geocode = pd.DataFrame(columns=['name', 'address', 'x', 'y'])
        none = None
        for idx, road in tqdm(zip(test_data.index, test_data['address'])):
            name = str(test_data['name'][idx])
            if len(str(road)) <= 5:
                geocode = geocode.append(
                    pd.DataFrame({'name': name,
                                  'address': road,
                                  'x': none,
                                  'y': none},
                                 index=[idx]))
                continue

            json_data = self.request_geo(road)

            if json_data['response']['status'] == 'NOT_FOUND' or json_data['response']['status'] == 'ERROR':
                geocode = geocode.append(
                    pd.DataFrame({'name': name,
                                  'address': road,
                                  'x': none,
                                  'y': none},
                                 index=[idx]))
                continue

            x = json_data['response']['result']['point']['x']
            y = json_data['response']['result']['point']['y']

            geocode = geocode.append(
                pd.DataFrame({'name': name,
                              'address': road,
                              'x': float(x),
                              'y': float(y)},
                             index=[idx]))
        return geocode

    def calculate_distance(self, coor1, coor2):
        """
        입력된 두 좌표(x, y)에 대해 거리를 계산하는 함수
        :param coor1: 좌표1
        :param coor2: 좌표2
        :return: 두 좌표 사이 거리
        """
        return haversine(coor1, coor2)

    def Optimal_Path_algorithm(self, test_data):
        """
        최적의 경로를 계산하는 함수
        :param test_data:
        :return:
        """
        result = self.extraction_geo(test_data)

        items = []
        for i in range(self.COURSE_SIZE):
            items.append((result.x[i], result.y[i]))

        list_distance_2dim = [] # 모든 여행지 사이의 거리를 담은 2차원 배열
        for i in range(self.COURSE_SIZE):
            list_distance = []
            for j in range(self.COURSE_SIZE):
                list_distance.append(self.calculate_distance(items[i], items[j]))
            list_distance_2dim.append(list_distance)

        a = [0, 1, 2, 3]
        permute_list = list(permutations(a, 4))

        print(permute_list)

        min_sum_distance = 10000000
        min_idx = 0
        for idx in range(len(permute_list)):
            i = permute_list[idx][0]
            j = permute_list[idx][1]
            k = permute_list[idx][2]
            l = permute_list[idx][3]

            idx_sum_distance = list_distance_2dim[i][j] + list_distance_2dim[j][k] + list_distance_2dim[k][l] # 해당 idx에서의 총 거리
            if idx_sum_distance < min_sum_distance:
                min_sum_distance = idx_sum_distance
                min_distance = [list_distance_2dim[i][j], list_distance_2dim[j][k], list_distance_2dim[k][l]]
                min_idx = permute_list[idx]

        self.data_course['sequence'] = list(min_idx)
        self.data_course['distance'] = list(min_distance)
        self.data_course['sum_distance'].append(min_sum_distance)

    def search_db_course(self, location: str, theme: str) -> dict:  # -> 는 return 값이 어떤 값인지 명시해주기 위함
        """
        데이터베이스에서 지역과 여행지를 검색합니다.

        :param location: 지역
        :param theme: 테마
        :return: 전체 여행지 정보(dict값)를 모아놓은 list
        """

        datas = self._make_query(location, theme)

        if len(datas) == 0:
            return -1; # 해당 query에 맞는 data가 존재하지 않는 경우
        elif len(datas) < 4:
            return -2; # 여행지가 4개 이상 존재하지 않는 경우(코스를 짤 수 없는 경우)

        # SELECT된 데이터 중에서 랜덤으로 하나 뽑기 위해 변수 설정
        # 최대치는 3번째 칸에 출력된 결과 까지이며, 너무 뒷쪽 결과는 출력하지 않음

        all_data = []
        all_data_list = []

        for rand_idx in self.select_travel(len(datas) - 1):
            data_dict_list = {
                # 데이터를 담을 딕셔너리 구조를 정의합니다.
                'idx': [], 'name': [],
                'tel': [], 'context': [],
                'category': [], 'address': [],
                'thumUrl': [], 'theme': []
            }

            data_dict = {
                # 데이터를 담을 딕셔너리 구조를 정의합니다.
                'idx': '', 'name': '',
                'tel': '', 'context': '',
                'category': '', 'address': '',
                'thumUrl': '', 'theme' :''
            }

            category_list = self.edit_category(datas[rand_idx]['category'])
            random_category_idx = randint(0, len(category_list) - 1)

            data_dict['idx'] = datas[rand_idx]['idx']
            data_dict['name']= datas[rand_idx]['name']
            data_dict['tel'] = datas[rand_idx]['tel']
            data_dict['context'] = datas[rand_idx]['name']  # context 관련 column이 없어서 일단 name 집어 넣음
            data_dict['category'] = category_list
            data_dict['address'] = datas[rand_idx]['address']
            data_dict['thumUrl'] = datas[rand_idx]['thumUrl']
            data_dict['theme'] = theme

            data_dict_list['idx'].append(datas[rand_idx]['idx'])
            data_dict_list['name'].append(datas[rand_idx]['name'])
            data_dict_list['tel'].append(datas[rand_idx]['tel'])
            data_dict_list['context'].append(datas[rand_idx]['name'])  # context 관련 column이 없어서 일단 name 집어 넣음
            data_dict_list['category'].append(category_list)
            data_dict_list['address'].append(datas[rand_idx]['address'])
            data_dict_list['thumUrl'].append(datas[rand_idx]['thumUrl'])
            data_dict_list['theme'].append(theme)

            all_data.append(data_dict)

            all_data_list.append(data_dict_list)

        self.test_data = pd.DataFrame(all_data, index=self.index)
        self.Optimal_Path_algorithm(self.test_data)

        self.data_dict_1 = all_data_list[self.data_course['sequence'][0]]
        self.data_dict_2 = all_data_list[self.data_course['sequence'][1]]
        self.data_dict_3 = all_data_list[self.data_course['sequence'][2]]
        self.data_dict_4 = all_data_list[self.data_course['sequence'][3]]

        self.data_dict_1 = self._flatten_dicts(self.data_dict_1)
        self.data_dict_2 = self._flatten_dicts(self.data_dict_2)
        self.data_dict_3 = self._flatten_dicts(self.data_dict_3)
        self.data_dict_4 = self._flatten_dicts(self.data_dict_4)

        return [self.data_dict_1, self.data_dict_2, self.data_dict_3, self.data_dict_4]