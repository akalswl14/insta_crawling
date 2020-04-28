import csv
import os
import pandas as pd
import numpy as np

ProjectFolder = os.getcwd()

def MakeExcel(DataList):
    df = pd.DataFrame(DataList, columns=['FeedId','LikeNumber','Text','ImageList','VideoList'])
    df.to_excel('InstaCrawling.xlsx')
    print('크롤링 정보 저장 완료')

def MakeFollowerExcel(DataList):
    df = pd.DataFrame(DataList, columns=['followerid'])
    df.to_excel('FollowerList.xlsx')
    print('팔로워리스트 저장 완료')