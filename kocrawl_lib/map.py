"""
@auther Hyunwoong
@since {6/21/2020}
@see : https://github.com/gusdnd852
"""
from kocrawl.answerer.map_answerer import MapAnswerer
from kocrawl.base import BaseCrawler
from kocrawl.editor.map_editor import MapEditor
from kocrawl.searcher.map_searcher import MapSearcher

class MapCrawler(BaseCrawler):

    def __init__(self):
        self.map_dict = {}
        self.map_msg = ""

    def request(self, location: str, theme: str) -> str:
        """
        지도를 크롤링합니다.
        (try-catch로 에러가 나지 않는 함수)

        :param location: 지역
        :param theme: 테마
        :return: 해당지역 장소
        """

        map_tuple = self.request_debug(location, theme)
        self.map_msg = map_tuple[0]
        self.map_dict = map_tuple[1]

        try:
            return self.map_msg
        except Exception:
            return MapAnswerer().sorry(
                "해당 지역은 알 수 없습니다."
            )

    def request_dict(self, location: str, theme: str):
        """
        지도를 크롤링합니다.
        (try-catch로 에러가 나지 않는 함수)

        :param location: 지역
        :param theme: 테마
        :return: 해당지역 장소
        """

        try:
            return self.request_debug(location, theme)[1]
        except Exception:
            return MapAnswerer().sorry(
                "해당 지역은 알 수 없습니다."
            )

    def request_debug(self, location: str, theme: str) -> tuple:
        """
        지도를 크롤링합니다.
        (에러가 나는 디버깅용 함수)

        :param location: 지역
        :param theme: 테마
        :return: 해당지역 장소
        """

        result_dict = MapSearcher().search_db_map(location, theme)
        result = MapEditor().edit_map(location, theme, result_dict)
        result = MapAnswerer().map_form(location, theme, result)

        return result, result_dict