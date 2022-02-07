"""
@auther Hyunwoong
@since {6/21/2020}
@see : https://github.com/gusdnd852
"""
from kocrawl.answerer.base_answerer import BaseAnswerer

class MapAnswerer(BaseAnswerer):

    def map_form(self, location: str, theme: str, result: dict) -> str:
        """
        여행지 출력 포맷

        :param location: 지역
        :param place: 테마
        :param result: 데이터 딕셔너리
        :return: 출력 메시지
        """

        if result['theme'] != '' and result['theme'] != '관광지': # 테마가 입력 됐을 때
            msg = self.map_init_theme.format(location=location, theme=theme)
            msg += '<br><br>{location} 여행지 중 '
            msg = self._add_msg_from_dict(result, 'theme', msg, '{theme}와(과) 관련있는 ')
        else: # 테마가 입력되지 않았을
            # 때
            msg = self.map_init.format(location=location, theme=theme)
            msg += '<br><br>{location} 여행지 중 '

        msg = self._add_msg_from_dict(result, 'name', msg, '{name}에 가보시는 건 어떤가요?<br>')
        msg = self._add_msg_from_dict(result, 'address', msg, '주소는 {address}에 위치해있어요<br>')
        msg = self._add_msg_from_dict(result, 'category', msg, '<br>{category}<br>')
        msg += '<br>이 여행지를 자세히 알고싶다면 '
        msg += '<a href="http://127.0.0.1:8080/DetailPage" target="_blank">여기</a>'
        msg += '를 눌러주세요~<br>'
        msg = msg.format(location=location, category=result['category'],
                         name=result['name'], address=result['address'], thumUrl=result['thumUrl'],
                         theme=result['theme'])

        return msg