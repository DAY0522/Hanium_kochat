"""
@auther Hyunwoong
@since {6/21/2020}
@see : https://github.com/gusdnd852
"""

# 일단 map_answerer 복붙함
from kocrawl.answerer.base_answerer import BaseAnswerer

class CourseAnswerer(BaseAnswerer):

    def course_form(self, location: str, theme: str, result: list) -> str:
        """
        여행지 출력 포맷

        :param location: 지역
        :param theme: 테마
        :param result: 데이터 딕셔너리
        :return: 출력 메시지
        """

        msg = self.course_init.format(location=location, theme=theme)

        msg += '<br><br>{location}에 위치한 {theme} 여행 코스를 알려드릴게요!'

        msg = self._add_msg_from_dict(result[0], 'name', msg, '<br>\'{name_0} → ')
        msg = self._add_msg_from_dict(result[1], 'name', msg, '{name_1} → ')
        msg = self._add_msg_from_dict(result[2], 'name', msg, '{name_2} → ')
        msg = self._add_msg_from_dict(result[3], 'name', msg, '{name_3}\' 코스는 어떠신가요?<br>')

        msg += '<br>이 코스를 자세히 알고싶다면 '
        msg += '<a href="http://127.0.0.1:8080/Course" target="_blank">여기</a>'
        msg += '를 눌러주세요~<br>'

        msg = msg.format(location=location, category=result[0]['category'], name_0=result[0]['name'],
                         name_1=result[1]['name'], name_2=result[2]['name'], name_3=result[3]['name'],
                         address=result[0]['address'], thumUrl=result[0]['thumUrl'],
                         theme=result[0]['theme'])

        return msg