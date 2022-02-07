"""
@auther Hyunwoong
@since {6/21/2020}
@see : https://github.com/gusdnd852
"""

# 일단 map_editor 복붙함
from kocrawl.editor.base_editor import BaseEditor
import re


class CourseEditor(BaseEditor):

    def edit_course(self, location: str, theme: str, result: list) -> list:
        """
        join_dict를 사용하여 딕셔너리에 있는 string 배열들을
        하나의 string으로 join합니다.

        :param location: 지역
        :param theme: 테마
        :param result: 데이터 딕셔너리
        :return: 수정된 딕셔너리
        """

        result_list = []
        for i in range(len(result)):
            result[i] = self.join_dict(result[i], 'name')
            result[i] = self.join_dict(result[i], 'tel')
            result[i] = self.join_dict(result[i], 'context')
            result[i] = self.join_dict(result[i], 'category')
            result[i] = self.join_dict(result[i], 'address')
            result[i] = self.join_dict(result[i], 'thumUrl')
            result[i] = self.join_dict(result[i], 'theme')

            if isinstance(result[i]['context'], str):
                result[i]['context'] = re.sub(' ', ', ', result[i]['context'])
            result_list.append(result[i])

        return result_list
