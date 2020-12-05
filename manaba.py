import yaml
import requests
import time
import os
from dotenv import load_dotenv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.keys import Keys

#envファイル読み込み
load_dotenv()

URL = "http://www.ritsumei.ac.jp/ct/"
Selector = "#btnLogin"

driver = webdriver.Chrome()
driver.get(URL)

driver.find_element_by_id('btnLogin').click()
time.sleep(3)

#立命館のmanabaはタブが謎に遷移するのでそれに対応
driver.switch_to.window(driver.window_handles[-1])
print(os.environ['USERID'])

#値入力
driver.find_element_by_id('User_ID').send_keys(os.environ['USERID'])
driver.find_element_by_id('Password').send_keys(os.environ['PASSWORD'])
#ログイン
driver.find_element_by_id("Submit").click()
