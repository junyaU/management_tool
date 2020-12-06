import yaml
import requests
import time
import os
from manaba_login import LoginManaba
from dotenv import load_dotenv
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait

from selenium.webdriver.common.keys import Keys

class GetKadaiData:
  #envファイル読み込み
  load_dotenv()
  def __init__(self):
    self.base_url = os.environ['BASE_URL']
    self.LoginManaba = LoginManaba()


  def getKadai(self):
    mypage = self.LoginManaba.login()
    soup = BeautifulSoup(mypage, features="html.parser")
    #授業のデータ
    class_datas = soup.select('.course-cell')

    for data in class_datas:
      #授業の詳細URL
      class_url = self.base_url + data.find("a").get("href")
      response = requests.get(class_url).text

      print(response)




GetKadaiData().getKadai()