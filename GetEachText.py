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

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

warnings.filterwarnings(action='ignore')  # 경고 메세지 제거

#현재 프로젝트 폴더
ProjectFolder = os.getcwd()

# 인스타 그램 url 생성
baseUrl = "https://www.instagram.com"


def EachFeed(driver, FeedUrlList):
    FeedDataList = []
    for EachUrl in FeedUrlList:
        FeedDataList.append(GetEachContents(driver, EachUrl))
    return FeedDataList


def GetEachContents(driver, EachUrl):
    FeedData = []
    url = baseUrl+str(EachUrl)
    driver.get(url)
    sleep(3)
    try:
        driver.find_element(
            By.XPATH, '//*[@id="react-root"]/section/nav/div/div/section/div/div[2]/div[4]/button').click()
        driver.find_element(
            By.XPATH, '//*[@id="react-root"]/section/nav/div/div/section/div[3]/button[2]').click()
    except:
        pass
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".sXUSN"))
        )
    except:
        pass
    else:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/div/div/span/span[2]/button'))
        )
        driver.find_element(By.XPATH, '//*[@id="react-root"]/section/main/div/div/article/div[2]/div[1]/div/div/span/span[2]/button').click()

    pageString = driver.page_source
    soup = BeautifulSoup(pageString, "lxml")
    TextSection = soup.select("._8Pl3R")[0].text
    try : 
        LikeNum = soup.select("div.Nm9Fw span")[0].text
    except :
        try : 
            LikeNum = soup.select(".zV_Nj")[0].text[4]
        except :
            driver.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/div/article/div[2]/section[2]/div/span').click()
            pageString = driver.page_source
            soup = BeautifulSoup(pageString, "lxml")
            LikeNum = soup.select('.vJRqr')[0].text[4]

    #feedid
    FeedData.append(EachUrl[3:])

    #likenum
    FeedData.append(LikeNum)

    #text
    FeedData.append(TextSection)

    image = list()
    if(driver.find_elements_by_css_selector(".coreSpriteRightChevron") or driver.find_elements(By.CLASS_NAME,"vi798")):
        while(True):
            pageString = driver.page_source
            soup = BeautifulSoup(pageString, "lxml")
            LiTagList = soup.select(".FFVAD")
            LiTagList += soup.select(".tWeCl")
            if len(LiTagList) == 0 :
                driver.get(url)
                continue
            try:
                for LiTag in LiTagList:
                    image.append(LiTag.attrs['src'])
            except KeyError as keyerr:
                print(keyerr)
                print(LiTag)
                print("!!!!!!!KEYERROR!!!!!!!!!")
                driver.get(url)
                continue
            if(driver.find_elements_by_css_selector(".coreSpriteRightChevron")):
                driver.find_element_by_css_selector(".coreSpriteRightChevron").click()
                sleep(1)
                print("click")
            else:
                break
    else:
        while(True):
            pageString = driver.page_source
            soup = BeautifulSoup(pageString, "lxml")
            EachContent = soup.select(".FFVAD") + soup.select(".tWeCl")
            if len(EachContent) == 0:
                driver.get(url)
                continue
            else:
                image.append(EachContent[0].attrs['src'])
                break

    image = list(set(image))
    imgList = []
    vidList = []
    
    for img in image:
        if ".mp4" in img :
            vidList.append(img)
        else :
            imgList.append(img)
    #imglist
    FeedData.append(imgList)

    #videolist
    FeedData.append(vidList)
    print("------------------------------")
    return FeedData
