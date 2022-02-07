import pandas as pd     # pip install pands필요
import numpy as np
import os


# xpath 존재 유무 확인
def has_xpath(driver, xpath):
    try:
        driver.find_element_by_xpath(xpath)
        return True
    except:
        return False

def has_selector(driver, selector):
    try:
        driver.find_element_by_css_selector(selector)
        return True
    except:
        return False

def has_id(driver, id):
    try:
        driver.find_element_by_id(id)
        return True
    except:
        return False

def make_excel(df, name_csv): # 저장된 딕셔너리를 엑셀로 만들어주는 함수
    # .to_csv
    # 이미 csv 파일이 존재하면 그 아래 component들을 추가(mode가 a)
    # 존재하지 않으면 새로 생성(mode가 w)
    if not os.path.exists(name_csv + ".csv"):
        df.to_csv(name_csv + ".csv", index=False, mode='w', encoding='utf-8-sig')
    else:
        df.to_csv(name_csv + ".csv", index=False, mode='a', encoding='utf-8-sig', header=False)

    # 해당이름의 csv파일을 읽어옴
    r_csv = pd.read_csv(name_csv + ".csv")

    # 저장할 xlsx파일의 이름을 정함
    save_xlsx = pd.ExcelWriter(name_csv + ".xlsx")

    r_csv.to_excel(save_xlsx, index = False) # xlsx 파일로 변환
    save_xlsx.save() #xlsx 파일로 저장

def csv_from_xlsx(name_xlsx):
    xlsx = pd.read_excel(name_xlsx + ".xlsx")
    xlsx.to_csv(name_xlsx + ".csv")

def xlsx_from_csv(name_csv):
    xlsx = pd.read_csv(name_csv + ".csv")
    xlsx.to_xlsx(name_csv + ".xlsx")
