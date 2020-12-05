import yaml
import requests
import time
import os
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.keys import Keys

class LoginManaba:
  #envファイル読み込み
  load_dotenv()
  def __init__(self):
    self.env = os.environ

  def login(self):
    op = Options()
    op.add_argument("--disable-gpu")
    op.add_argument("--disable-extensions")
    op.add_argument("--proxy-server='direct://'")
    op.add_argument("--proxy-bypass-list=*")
    op.add_argument("--start-maximized")
    op.add_argument("--headless")
    URL = "http://www.ritsumei.ac.jp/ct/"

    driver = webdriver.Chrome(chrome_options=op)
    driver.get(URL)

    driver.find_element_by_id('btnLogin').click()
    time.sleep(3)

    #立命館のmanabaはタブが謎に遷移するのでそれに対応
    driver.switch_to.window(driver.window_handles[-1])
    time.sleep(1)

    #値入力
    driver.find_element_by_id('User_ID').send_keys(self.env['USERID'])
    driver.find_element_by_id('Password').send_keys(self.env['PASSWORD'])
    #ログイン
    driver.find_element_by_id("Submit").click()
    time.sleep(3)

    driver.find_element_by_class_name("mynavi-button-course").click()

    return driver.page_source.encode('utf-8')

  def aaa(self):
    login_page = self.login()

    soup = BeautifulSoup(login_page, features="html.parser")
    class_datas = soup.select('.course-cell')
