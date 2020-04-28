import os
import urllib.request
from urllib.request import urlopen  # 인터넷 url를 열어주는 패키지
from urllib.parse import quote_plus  # 한글을 유니코드 형식으로 변환해줌
from bs4 import BeautifulSoup
from selenium import webdriver  # webdriver 가져오기
import time  # 크롤링 중 시간 대기를 위한 패키지
from time import sleep
import warnings  # 경고메시지 제거 패키지
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.chrome.options import Options
from ScrollFeed import ScrollFeed
from GetEachText import GetEachContents,EachFeed
from MakeExcel import MakeExcel


warnings.filterwarnings(action='ignore')  # 경고 메세지 제거

StartTime = time.time()

#현재 프로젝트 폴더
ProjectFolder = os.getcwd()


options = webdriver.ChromeOptions()
mobile_emulation = {"deviceName": "Nexus 5"}
options.add_experimental_option("mobileEmulation", mobile_emulation)


driver = webdriver.Chrome(
    executable_path=ProjectFolder+"/chromedriver", chrome_options=options
)

instaId = 'stylebox2u'
# FeedUrlList = ['p/B-enhBhg3PR/']
FeedUrlList = ScrollFeed(driver,instaId)
FeedDataList = EachFeed(driver,FeedUrlList)
MakeExcel(FeedDataList)
driver.close()
print("소요시간 : ", time.time()-StartTime)
