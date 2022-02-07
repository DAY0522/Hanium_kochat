"""
@auther Hyunwoong
@since {6/21/2020}
@see : https://github.com/gusdnd852
"""
from random import randint
from kocrawl.searcher.base_searcher import BaseSearcher

import pymysql
import random

# DB 접속
connect = pymysql.connect(host='haniumdb1.cclzfuhgqdpp.ap-northeast-2.rds.amazonaws.com', user='admin', password='kkklp1720', db='hanium', charset='utf8')
cur = connect.cursor(pymysql.cursors.DictCursor)

class MapSearcher(BaseSearcher):

   def __init__(self):
      self.data_dict = {
         # 데이터를 담을 딕셔너리 구조를 정의합니다.
         'idx': [], 'name': [],
         'tel': [], 'context': [],
         'category': [], 'address': [],
         'thumUrl': [],'theme' : []
      }

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

   def search_db_map(self, location: str, theme: str) -> dict: # -> 는 return 값이 어떤 값인지 명시해주기 위함
      """
      데이터베이스에서 지역과 여행지를 검색합니다.

      :param location: 지역
      :param theme: 테마
      :return: 사용할 내용만 json에서 뽑아서 dictionary로 만듬.
      """

      # db에서 검색하기 위해 query문을 만듦

      datas = self._make_query(location, theme)
      random_idx = randint(0, len(datas)-1)


      # SELECT된 데이터 중에서 랜덤으로 하나 뽑기 위해 변수 설정
      # 최대치는 3번째 칸에 출력된 결과 까지이며, 너무 뒷쪽 결과는 출력하지 않음

      category_list = self.edit_category(datas[random_idx]['category'])
      random_category_idx = randint(0, len(category_list)-1)

      self.data_dict['idx'].append(datas[random_idx]['idx'])
      self.data_dict['name'].append(datas[random_idx]['name'])
      self.data_dict['tel'].append(datas[random_idx]['tel'])
      self.data_dict['context'].append(datas[random_idx]['name']) # context 관련 column이 없어서 일단 name 집어 넣음
      self.data_dict['category'].append(category_list)
      self.data_dict['address'].append(datas[random_idx]['address'])
      self.data_dict['thumUrl'].append(datas[random_idx]['thumUrl'])
      self.data_dict['theme'].append(theme)
      self.data_dict = self._flatten_dicts(self.data_dict)

      return self.data_dict