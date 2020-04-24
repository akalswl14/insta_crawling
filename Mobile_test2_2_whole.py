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

StartTime = time.time()

#현재 프로젝트 폴더
ProjectFolder = os.getcwd()

# 인스타 그램 url 생성
baseUrl = "https://www.instagram.com/"
plusUrl = 'stylebox2u'
url = baseUrl + quote_plus(plusUrl)

options = webdriver.ChromeOptions()
mobile_emulation = {"deviceName": "Nexus 5"}
options.add_experimental_option("mobileEmulation", mobile_emulation)


driver = webdriver.Chrome(
    executable_path="/Users/carly/Development/crawling/chromedriver", chrome_options=options
)
driver.get(url)

time.sleep(3)

# # 로그인 하기
# print('로그인 중 입니다.')
# login_section = '//*[@id="react-root"]/section/nav/div/div/div[2]/div/div/div/a[1]'

# driver.find_element_by_xpath(login_section).click()
# time.sleep(2)


# elem_login = driver.find_element_by_name("username")
# elem_login.clear()
# elem_login.send_keys('WRITE_YOUR_ID')

# elem_login = driver.find_element_by_name('password')
# elem_login.clear()
# elem_login.send_keys('WRITE_YOUR_PASSWORD')

# time.sleep(1)
# xpath = '//*[@id="react-root"]/section/main/article/div/div/div/form/div[7]/button'
# driver.find_element_by_xpath(xpath).click()

# time.sleep(1)

# # try:
# xpath = '//*[@id="react-root"]/section/main/div/div/div/button'
# driver.find_element_by_xpath(xpath).click()
# # except:
#     # pass
# time.sleep(4)

#스크롤하기
SCROLL_PAUSE_TIME = 1.0
reallink = []  # 게시물 url 리스트

pageString = driver.page_source
soup = BeautifulSoup(pageString, "lxml")
OriginalPostNum = int(soup.select('.g47SY.lOXF2')[0].text)
print("포스트 갯수는 원래 " + str(OriginalPostNum)+"개 입니다.")

while True:
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
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        sleep(SCROLL_PAUSE_TIME)
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            reallink = list(set(reallink))
            if (len(reallink) != OriginalPostNum):
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

# reallink = ['/p/B907FfcAH2p/']
# reallink = ['/p/B83J79PA2G8/']

EmptyFolder = 0

for i in reallink:

    url = 'https://www.instagram.com/'+str(i)
    driver.get(url)
    driver.find_element(By.CSS_SELECTOR, "._97aPb > div:nth-child(1)").click()
    sleep(2)

    #저장할 폴더 경로
    f_url = ProjectFolder + '/MobileTest_img/'+i[3:]
    #폴더 있으면 삭제
    if(os.path.isdir(f_url)):
        print('이미 다운받은 게시글입니다.')
        continue
    #저장할 폴더 생성
    else:
        os.mkdir(f_url)

    print(f_url+'을 작업중입니다.')
    # ImgList = []
    # VidList = []

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
driver.close()

print('콘텐츠 저장 완료')

print("빈 폴더는 "+str(EmptyFolder)+"개 입니다.")

print("소요시간 : ", time.time()-StartTime)
