#!/usr/bin/python
# -*- coding: utf-8 -*-
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pprint
from selenium import webdriver
import time
from datetime import datetime, timedelta
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select
import chromedriver_autoinstaller


chromedriver_autoinstaller.install()


# 어드민 정보
f = open("account.txt")
lines = f.readlines()
admin_id = lines[0].strip()
admin_pw = lines[1].strip()
f.close()

# 구글 시트 접속
scope = ["https://spreadsheets.google.com/feeds", 'https://www.googleapis.com/auth/spreadsheets',
         "https://www.googleapis.com/auth/drive.file", "https://www.googleapis.com/auth/drive"]
creds = ServiceAccountCredentials.from_json_keyfile_name("creds.json", scope)
client = gspread.authorize(creds)
sheet = client.open('멸망전 지표').worksheet("RAW")

ids = sheet.col_values(1)
date = sheet.col_values(2)

del ids[0]
del date[0]
s_date = date[0]
search_date = datetime.strptime(s_date,"%Y-%m-%d")
search_date2 = datetime.strptime(s_date,"%Y-%m-%d") + timedelta(days=1)

search_date = str(search_date)[:10]
search_date2 = str(search_date2)[:10]
pprint.pprint(search_date)
pprint.pprint(search_date2)
pprint.pprint(ids)
pprint.pprint(search_date)



webDriver_options = webdriver.ChromeOptions()
webDriver_options .add_argument('headless')
DRIVER_PATH = './chromedriver.exe'
driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=webDriver_options)

# 닉네임 구하기
nicks = {}
for id in ids:
    BJ_URL = "https://afreecatv.com/"+str(id)
    driver.get(BJ_URL)
    time.sleep(1)
    try:
        BJ_NAME_XPATH = '//*[@id="bs-navi"]/div/article[1]/section/div/div[1]/h2'
        name = driver.find_element_by_xpath(BJ_NAME_XPATH).text
        nicks[id] = name
    except NoSuchElementException as e:
        continue
    print(nicks)


# 어드민 로그인 하기
admin_login_URL = "https://login.afreecatv.com/afreeca/login.php?szFrom=full&request_uri=http://admin.afreecatv.com/app/broad_log.php"
driver.get(admin_login_URL)
time.sleep(1)
idBox = driver.find_element_by_css_selector("#uid")
idBox.send_keys(admin_id)
pwBox = driver.find_element_by_css_selector("#password")
pwBox.send_keys(admin_pw)
loginBox = driver.find_element_by_css_selector("body > form:nth-child(11) > div > fieldset > p.login_btn > button").click()
time.sleep(2)
# 어드민 검색 조건 설정
setting_cal = driver.find_element_by_css_selector("#start_date")
setting_cal.clear()
setting_cal.send_keys(search_date)
setting_cal = driver.find_element_by_css_selector("#end_date")
setting_cal.clear()
setting_cal.send_keys(search_date2)
time.sleep(2)
select = Select(driver.find_element_by_css_selector("#order_by"))
select.select_by_index(3)
select = Select(driver.find_element_by_css_selector("#sort_by"))
select.select_by_index(0)
time.sleep(2)


info = {}
# 어드민 시작시간 찾기
for id in ids:
    input_id = driver.find_element_by_css_selector("#user_id")
    input_id.clear()
    input_id.send_keys(id)
    driver.find_element_by_css_selector("#btnSearch").click()
    time.sleep(3)
    try:
        title = driver.find_element_by_xpath('/html/body/div[1]/div[5]/table/tbody/tr[1]/td[7]').text
        topTraffic = driver.find_element_by_xpath('/html/body/div[1]/div[5]/table/tbody/tr[1]/td[5]').text
        highTraffic = driver.find_element_by_xpath('/html/body/div[1]/div[5]/table/tbody/tr[1]/td[4]').text
        a = str(title)
        b = topTraffic.find('(')-1
        c = topTraffic[:b]
        d = highTraffic.find('(') - 1
        e = highTraffic[:d]
        info[id] = [a, e, c]
    except NoSuchElementException as e:
        continue
    time.sleep(1)
    print(info)

driver.close()

infoToList =[]
for k,v in info.items():
    for e, a in nicks.items():
        if k == e:
            b = [k, a, v[0],v[1],v[2]]
            infoToList.append(b)
        else:
            pass
print(infoToList)

j = 1
for i in infoToList:
    print(i)
    sheet.update_cell(j, 4, i[0])
    time.sleep(1)
    sheet.update_cell(j, 5, i[1])
    time.sleep(1)
    sheet.update_cell(j, 6, i[2])
    time.sleep(1)
    sheet.update_cell(j, 7, i[3])
    time.sleep(1)
    sheet.update_cell(j, 8, i[4])
    time.sleep(1)
    j += 1

