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
    self.op = Options()
    self.op.add_argument("--disable-gpu")
    self.op.add_argument("--disable-extensions")
    self.op.add_argument("--proxy-server='direct://'")
    self.op.add_argument("--proxy-bypass-list=*")
    self.op.add_argument("--start-maximized")
    self.op.add_argument("--headless")
    self.base_url = os.environ['BASE_URL']
    self.driver = webdriver.Chrome(chrome_options=self.op)
    self.driver.get("http://www.ritsumei.ac.jp/ct/")

  def login(self):
    driver = self.driver

    driver.find_element_by_id('btnLogin').click()
    time.sleep(3)

    #立命館のmanabaはタブが謎に遷移するのでそれに対応
    driver.switch_to.window(self.driver.window_handles[-1])
    time.sleep(1)

    #値入力
    driver.find_element_by_id('User_ID').send_keys(self.env['USERID'])
    driver.find_element_by_id('Password').send_keys(self.env['PASSWORD'])
    #ログイン
    driver.find_element_by_id("Submit").click()
    time.sleep(3)

    driver.find_element_by_class_name("mynavi-button-course").click()
  def getReportData(self):
    self.login()
    driver = self.driver
    class_urls = []
    class_datas = driver.find_elements_by_class_name('course-cell')
    print("レポートのデータ")

    #配列にURL格納
    for data in class_datas:
      data_url = data.find_element_by_tag_name('a').get_attribute('href') + '_report'
      class_urls.append(data_url)

    for class_url in class_urls:
      driver.get(class_url)
      soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')

      report_datas = soup.find_all('tr')
      for report_data in report_datas:
        if report_data:
          #まだ課題の受付をしていて且つ、未提出であるか
          within_the_deadline = report_data.find('span', class_='deadline')
          if within_the_deadline:
            suject_name = soup.select_one('#coursename').text
            report_name = report_data.find('a').text
            submission_deadline = report_data.find_all('td')[3].text
            print(suject_name, ':',report_name,':',submission_deadline+'まで')

  def getLittleTestData(self):
    self.login()
    driver = self.driver
    test_urls = []
    test_datas = driver.find_elements_by_class_name('course-cell')
    print("小テストのデータ")

    #配列にURL格納
    for data in test_datas:
      data_url = data.find_element_by_tag_name('a').get_attribute('href') + '_query'
      test_urls.append(data_url)

    for test_url in test_urls:
      driver.get(test_url)
      soup = BeautifulSoup(driver.page_source.encode('utf-8'), 'html.parser')

      soup_datas = soup.find_all('tr')
      for data in soup_datas:
        if data:
          #まだ課題の受付をしていて且つ、未提出であるか
          within_the_deadline = data.find('span', class_='deadline')
          if within_the_deadline:
            subject_name = soup.select_one('#coursename').text
            test_name = data.find('h3').find('a').text
            submission_deadline = data.find_all('td')[3].text
            print(subject_name,':',test_name,':',submission_deadline,'まで')

LoginManaba().getReportData()
LoginManaba().getLittleTestData()