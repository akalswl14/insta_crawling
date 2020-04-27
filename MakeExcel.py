import csv
import os
import pandas as pd
import numpy as np

ProjectFolder = os.getcwd()

def MakeExcel(DataList):
    df = pd.DataFrame(DataList, columns=['FeedId','LikeNumber','Text','ImageList','VideoList'])
    df.to_excel('InstaCrawling.xlsx')