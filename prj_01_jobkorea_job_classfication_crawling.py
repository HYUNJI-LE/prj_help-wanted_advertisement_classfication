# -*- coding: utf-8 -*-
"""Project_01_job_classfication_crawling.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/16qpqURM3c2e3sKJBopftSp52VLyEUkNC
"""

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
import time
import pandas as pd
import re
import ssl
import os, subprocess
import sys
options = webdriver.ChromeOptions()

options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('disable-gpu')
options.add_argument('lang=ko_KR')
driver = webdriver.Chrome('./chromedriver', options=options)

url = 'http://www.jobkorea.co.kr/recruit/joblist?menucode=duty'

try:
  driver.get(url)     
  time.sleep(0.3)     
  title = driver.find_element_by_xpath('//*[@id="dev-gi-list"]/div/div[5]/table/tbody/tr[1]/td[2]/div/strong/a').text      
  title =  re.compile('[^가-힣|a-z|A-Z|0-9]+').sub(' ', title)
  print(title)
except NoSuchElementException:
  print('NoSuchElementException')

category = ['Clerical work', 'Marketing', 'IT', 'Design', 'Trade', 'Sales work', 'Education','Medical']


page = [616, 198, 598, 205, 346,802 ]

spec_category = [2,3,6,9,4,5,3,4]

#전체버튼 누른 후 나온 첫 페이지에서 처음부터 100페이지로 주소 입력해서 넘어가면 안넘어가지는 경우가 있어서 다음 버튼을 눌러서 페이지를 10페이지로 옮긴 다음에 주소를 입력하게 했음 
driver = webdriver.Chrome('chromedriver', options=options)
df_titles = pd.DataFrame()
for a in range(1, 7):

    df_section_titles = pd.DataFrame()
    title_list = []
    driver.get(url)
    time.sleep(0.7)
    # 카테고리 선택
    driver.find_element_by_xpath(
        '//*[@id="devSearchForm"]/div[2]/div/div[1]/dl[1]/dd[2]/div[2]/dl[1]/dd/div[1]/ul/li[{0}]/label/span/span'.format(
            a)).click()
    time.sleep(0.5)
    # 세부 카테고리 전체 다 선택
    b = spec_category[a - 1]
    for c in range(1, 18):  
        try:
            driver.find_element_by_xpath(
                '//*[@id="duty_step2_1001{0}_ly"]/li[{1}]/label/span/span'.format(b, c)).click()

        except NoSuchElementException:
            print('NoSuchElementException')
    
    driver.find_element_by_xpath('//*[@id="dev-btn-search"]').click()
    time.sleep(1.0)
    # 페이지
    driver.find_element_by_xpath('//*[@id="dvGIPaging"]/div/p/a').click()
    time.sleep(0.7)
    for m in range(1,100):
        try:
            
            driver.get('http://www.jobkorea.co.kr/recruit/joblist?menucode=duty#anchorGICnt_{0}'.format(m))
            time.sleep(1.0)
                # 공고 제목 읽어오기
            for k in range(1, 41):
                try:
                    title = driver.find_element_by_xpath(
                        '//*[@id="dev-gi-list"]/div/div[5]/table/tbody/tr[{0}]/td[2]/div/strong/a'.format(k)).text
                    time.sleep(0.7)
                    title = re.compile('[^가-힣|a-z|A-Z|0-9]+').sub(' ', title)
                    print(title)
                    title_list.append(title)

                except NoSuchElementException:
                    print('NoSuchElementException')
        except NoSuchElementException:
            print('NoSuchElementException')
    # 카테고리 선택 초기화
    driver.find_element_by_xpath('//*[@id="content"]/div[1]/ul/li[2]/a').click()

    df_section_titles = pd.DataFrame(title_list)
    df_section_titles['category'] = category[a - 1]
    df_titles = pd.concat([df_titles, df_section_titles], axis=0, ignore_index=True)

"""
#나중에 교육, 메디칼 카테고리를 추가해서 카테고리별로 따로 크롤링할 때 사용한 코드 

driver = webdriver.Chrome('chromedriver', options=options)
df_titles = pd.DataFrame()


df_section_titles = pd.DataFrame()
title_list = []
driver.get(url)
time.sleep(0.7)
    # 카테고리 선택
driver.find_element_by_xpath('//*[@id="devSearchForm"]/div[2]/div/div[1]/dl[1]/dd[2]/div[2]/dl[1]/dd/div[1]/ul/li[10]/label/span/span').click()
time.sleep(0.5)
    # 세부 카테고리 전체 다 선택
b = spec_category[6]
for c in range(1, 10):  # (1,19)
        try:
            driver.find_element_by_xpath(
                '//*[@id="duty_step2_1002{0}_ly"]/li[{1}]/label/span/span'.format(b, c)).click()

        except NoSuchElementException:
            print('NoSuchElementException')

driver.find_element_by_xpath('//*[@id="dev-btn-search"]').click()
time.sleep(1.0)
# 페이지
driver.find_element_by_xpath('//*[@id="dvGIPaging"]/div/p/a').click()
time.sleep(0.7)
for m in range(150, 161):
        try:
            
            driver.get('http://www.jobkorea.co.kr/recruit/joblist?menucode=duty#anchorGICnt_{0}'.format(m))
                
            time.sleep(0.3)

                # 공고 제목 읽어오기
            for k in range(1, 41):
                try:
                    title = driver.find_element_by_xpath(
                        '//*[@id="dev-gi-list"]/div/div[5]/table/tbody/tr[{0}]/td[2]/div/strong/a'.format(k)).text
                    time.sleep(0.5)
                    title = re.compile('[^가-힣|a-z|A-Z|0-9]+').sub(' ', title)
                    print(title)
                    title_list.append(title)

                except NoSuchElementException:
                    print('NoSuchElementException')
        except NoSuchElementException:
            print('NoSuchElementException')
    # 카테고리 선택 초기화
driver.find_element_by_xpath('//*[@id="content"]/div[1]/ul/li[2]/a').click()

df_section_titles = pd.DataFrame(title_list)
df_section_titles['category'] = category[6]
df_titles = pd.concat([df_titles, df_section_titles], axis=0, ignore_index=True)
"""

#df_titles.to_csv('./help_wanted_advertisement_test3.csv')

print(df_titles.head())
print(df_titles.info())