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

from MakeExcel import MakeFollowerExcel
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


warnings.filterwarnings(action='ignore')  # 경고 메세지 제거

# 인스타 그램 url 생성
baseUrl = "https://www.instagram.com/"

SCROLL_PAUSE_TIME = 1.0

def Login(driver):
    # login_section = '//*[@id="react-root"]/section/nav/div/div/div[2]/div/div/div/a[1]'
    # driver.find_element_by_xpath(login_section).click()
    time.sleep(2)
    elem_login = driver.find_element_by_name("username")
    elem_login.clear()
    elem_login.send_keys('WRITE_YOUR_ID')
    elem_login = driver.find_element_by_name('password')
    elem_login.clear()
    elem_login.send_keys('WRITE_YOUR_PASSWORD')
    time.sleep(1)
    xpath = '//*[@id="react-root"]/section/main/article/div/div/div/form/div[7]/button'
    driver.find_element_by_xpath(xpath).click()
    time.sleep(3)
    # try:
    xpath = '//*[@id="react-root"]/section/main/div/div/div/button'
    driver.find_element_by_xpath(xpath).click()
    # except:
        # pass
    time.sleep(4)

def GetFollowers(driver,instaId):
    url = baseUrl + instaId
    driver.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/ul/li[2]/a').click()
    time.sleep(3)
    driver.find_element(By.XPATH,'/html/body/div[5]/div/div[2]/div/div/div/div[3]/a').click()
    Login(driver)
    driver.find_element(By.XPATH,'//*[@id="react-root"]/section/main/div/ul/li[2]/a').click()
    time.sleep(3)
    FollowerList = []
    while True:
        print('스크롤 하면서 Follower페이지의 끝을 찾는 중입니다.')
        pageString = driver.page_source
        soup = BeautifulSoup(pageString, "lxml")
        FollowerElementList = soup.select('.d7ByH')
        for follower in FollowerElementList :
            FollowerList.append(follower.text)

        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                FollowerList = list(set(FollowerList))
                print(str(len(FollowerList))+"개의 팔로워 수집")
                break
            else:
                last_height = new_height
                continue
    driver.get(url)
    # MakeFollowerExcel(FollowerList)
    return FollowerList

def ScrollFeed(driver, instaId):
    url = baseUrl + instaId
    driver.get(url)
    time.sleep(3)

    try : 
        xpath = '//*[@id="react-root"]/section/nav/div/div/section/div/div[2]/div[4]/button'
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
        driver.find_element(By.XPATH,xpath).click()
    except :
        pass
    pageString = driver.page_source
    soup = BeautifulSoup(pageString, "lxml")
    OriginalFollowerNum = soup.select('.g47SY.lOXF2')[1].attrs['title']
    OriginalFollowerNum = int(OriginalFollowerNum.replace(",",""))
    OriginalPostNum = soup.select('.g47SY.lOXF2')[0].text
    OriginalPostNum = int(OriginalPostNum.replace(",",""))

    print("팔로워 수는 원래 " + str(OriginalFollowerNum)+"개 입니다.")

    FollowerList = GetFollowers(driver,instaId)

    time.sleep(3)

    reallink = []  # 게시물 url 리스트

    pageString = driver.page_source
    soup = BeautifulSoup(pageString, "lxml")
    
    print("포스트 갯수는 원래 " + str(OriginalPostNum)+"개 입니다.")

    while True:
        try : 
            xpath = '//*[@id="react-root"]/section/nav/div/div/section/div/div[2]/div[4]/button'
            element = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
            driver.find_element(By.XPATH,xpath).click()
        except :
            pass
        print('스크롤 하면서 페이지의 끝을 찾는 중입니다.')
        pageString = driver.page_source
        bsObj = BeautifulSoup(pageString, "lxml")
        for link1 in bsObj.find_all(name="div", attrs={"class": "Nnq7C weEfm"}):
            atagLength = len(link1.select('a'))
            title = link1.select('a')[0]
            real = title.attrs['href']
            reallink.append(real)
            if(atagLength > 1):
                title = link1.select('a')[1]
                real = title.attrs['href']
                reallink.append(real)
                if(atagLength > 2):
                    title = link1.select('a')[2]
                    real = title.attrs['href']
                    reallink.append(real)

        last_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            sleep(SCROLL_PAUSE_TIME)
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                reallink = list(set(reallink))
                if (len(reallink) != OriginalPostNum): #원래 게시글 갯수와 다르면 다시 스크롤
                    driver.get(url)
                    continue
                else:
                    break
            else:
                last_height = new_height
                continue

    reallinknum = len(reallink)
    print("총"+str(reallinknum)+"개의 데이터.")

    #게시물 url 목록을 txt로 저장
    f = open('urllist.txt', 'w')
    f.write(str(reallink))
    f.close()
    print("txt저장성공")
    Logout(driver)
    return reallink

def Logout(driver):
    driver.find_element(By.XPATH,'//*[@id="react-root"]/section/nav/div/div/div[2]/div/div/div[5]/a').click()
    sleep(2)
    xpath = '//*[@id="react-root"]/section/nav[1]/div/header/div/div[1]/button'
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    driver.find_element(By.XPATH,xpath).click()
    xpath = '//*[@id="react-root"]/section/nav[1]/div/section/div[3]/div/div[4]/div/div/a'
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    driver.find_element(By.XPATH,xpath).click()
    xpath = '/html/body/div[4]/div/div/div[2]/button[1]'
    element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        )
    driver.find_element(By.XPATH,xpath).click()
    sleep(2)
