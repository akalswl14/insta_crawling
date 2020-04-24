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


warnings.filterwarnings(action='ignore')  # 경고 메세지 제거

#현재 프로젝트 폴더
ProjectFolder = os.getcwd()

# 인스타 그램 url 생성
baseUrl = "https://www.instagram.com/"

def EachFeed(driver, FeedUrlList):
    EmptyFolder = 0
    for EachUrl in FeedUrlList:
        EmptyFolder += GetEachContents(driver,EachUrl)

def GetEachContents(driver, EachUrl):
    EmptyFolder = 0
    url = baseUrl+str(EachUrl)
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, "._97aPb > div:nth-child(1)").click()
    sleep(2)

    #저장할 폴더 경로
    f_url = ProjectFolder + '/MobileTest_img/'+EachUrl[3:]
    #폴더 있으면 삭제
    if(os.path.isdir(f_url)):
        print('이미 다운받은 게시글입니다.')
        return EmptyFolder
    #저장할 폴더 생성
    else:
        os.mkdir(f_url)

    print(f_url+'을 작업중입니다.')

    image = list()
    # FirstOne = True
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
    cnt = 0
    image = list(set(image))
    for img in image:
        cnt += 1
        if(len(image) > 1):
            if ".mp4" in img:
                urllib.request.urlretrieve(img, f_url+str(cnt)+".mp4")
            else:
                urllib.request.urlretrieve(img, f_url+str(cnt)+".jpg")
        else:
            if ".mp4" in img:
                urllib.request.urlretrieve(img, f_url+str(cnt) + ".mp4")
            else:
                urllib.request.urlretrieve(img, f_url+str(cnt) + ".jpg")
    print(str(cnt)+"개의 게시글 콘텐츠를 폴더에 저장하였습니다.")
    if image == [] :
        EmptyFolder += 1
    print("------------------------------")
    return EmptyFolder