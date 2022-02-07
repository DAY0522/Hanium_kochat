from bs4 import BeautifulSoup
import requests

baseUrl = requests.get('https://search.naver.com/search.naver?ie=UTF-8&sm=whl_hty&query=%EC%84%9C%EC%9A%B8+%EB%A7%9B%EC%A7%91')

soup = BeautifulSoup(baseUrl.text, 'html.parser')
ul = soup.select_one('div.api_subject_bx > div > ul')
result = ul.select_one('li > div > a > div > div > span.OXiLu')

print(result)