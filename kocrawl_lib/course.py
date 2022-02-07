"""
@auther Hyunwoong
@since {6/21/2020}
@see : https://github.com/gusdnd852
"""
from kocrawl.answerer.course_answerer import CourseAnswerer
from kocrawl.base import BaseCrawler
from kocrawl.editor.course_editor import CourseEditor
from kocrawl.searcher.course_searcher import CourseSearcher


class CourseCrawler(BaseCrawler):

    def __init__(self):
        self.course_dict = {}
        self.course_msg = ""

    def request(self, location: str, theme: str) -> str:
        """
        지도를 크롤링합니다.
        (try-catch로 에러가 나지 않는 함수)

        :param location: 지역
        :param theme: 테마
        :return: 해당지역 장소
        """

        course_tuple = self.request_debug(location, theme)
        self.course_msg = course_tuple[0]
        self.course_dict = course_tuple[1]

        try:
            return self.course_msg
        except Exception:
            return CourseAnswerer().sorry(
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
            return CourseAnswerer().sorry(
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
        if CourseSearcher().search_db_course(location, theme) == -1:
            result = location + "에 해당 테마 여행지가 존재하지 않습니다.<br>다른 테마 및 지역을 입력해주세요."
            return result, {}
        elif CourseSearcher().search_db_course(location, theme) == -2:
            result = location + "에 해당 테마 여행 코스가 존재하지 않습니다.<br>그대신 " + location + "의 " + theme + "관련 여행지는 어떠세요?<br>" + theme + "여행지를 알고 싶다면 다음과 같이 채팅에 입력해주세요.<br>" + location + " " + theme + " 여행지 추천해줘"
            return result, {}
        else:
            result_dict_list = CourseSearcher().search_db_course(location, theme)
            result = CourseEditor().edit_course(location, theme, result_dict_list)
            result = CourseAnswerer().course_form(location, theme, result)

            return result, result_dict_list
