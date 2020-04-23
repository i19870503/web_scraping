# -*- coding: utf-8 -*-
"""
安居客房价爬虫
@author: i19870503
"""

import requests
import re
import time
import pandas as pd
import csv
import numpy as np
import math
import pymysql
import json
from tqdm import tqdm
from lxml import etree
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from scrapy.http import HtmlResponse
import datetime
import re
import time

from selenium.webdriver.chrome.options import Options
chrome_options = Options()
chrome_options.add_argument('--headless')

def crawl_house_price():
    loopNum = 0
    ifHandle = False
    pageNum = 100
    while(pageNum >= 1):
        loopNum = loopNum + 1
        if (len(re.findall(u'下一页', driver.page_source)) == 0):
            break
    
        target = driver.find_element_by_class_name('multi-page')
        y = target.location['y']
        y = y - 100
        js = "var q=document.documentElement.scrollTop=" + str(y)
        driver.execute_script(js)
        time.sleep(1)
        if u"下一页" in driver.page_source:
            if ifHandle == False:
                crawl_price(driver.page_source)

                ifHandle = True
                try:
                    if(u"下一页" in driver.page_source):
                        pageNum = pageNum - 1
                        driver.find_element_by_partial_link_text("下一页").click()
                        ifHandle = False
                        loopNum = 0
                        time.sleep(1)
                        print("Page:" + str(pageNum))
                        num1 = 100 - pageNum + 1
                        print('num1 = ' + str(num1))
                except:
                    pageNum += 1

                
def crawl_price(page_source):
    response1 = HtmlResponse(url="my HTML string", body=driver.page_source, encoding="utf-8")
    tweet_nodes = response1.xpath('//*[@id="houselist-mod-new"]/li')
    i = 1
    #fo = open('house_price.txt', 'w')


    for tweet_node in tweet_nodes:
        #print(tweet_node)
        try:
            name = tweet_node.xpath('//*[@id="houselist-mod-new"]/li['+str(i)+']/div[2]/div[1]/a/text()').extract()[0]
            #info = '//*[@id="houselist-mod-new"]/li['+i+']/div[2]/div[1]'
            price = tweet_node.xpath('//*[@id="houselist-mod-new"]/li['+ str(i) +']/div[3]/span[1]/strong/text()').extract()[0]
            univalence = tweet_node.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[3]/span[2]/text()').extract()[0]
            location = response1.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[2]/div[3]/span/text()').extract()[0]
            layout = response1.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[2]/div[2]/span[1]/text()').extract()[0]
            size = response1.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[2]/div[2]/span[2]/text()').extract()[0]
            age = response1.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[2]/div[2]/span[4]/text()').extract()[0]
            floor = response1.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[2]/div[2]/span[3]/text()').extract()[0]
            city = tweet_node.xpath('//*[@id="switch_apf_id_7"]/span[1]/text()').extract()[0]
            region = location.strip().split('\n')[1].strip()
            address = location.strip().split('\n')[0].strip()

            print(name.strip(), price.strip() + "万", univalence.strip(), city.strip(), region, address, layout.strip(),
                  size.strip(), age.strip(), floor.strip(), sep = '\t')
            i += 1
        except IndexError:
            name = tweet_node.xpath('//*[@id="houselist-mod-new"]/li['+str(i)+']/div[2]/div[1]/a/text()').extract()[0]
            #info = '//*[@id="houselist-mod-new"]/li['+i+']/div[2]/div[1]'
            price = tweet_node.xpath('//*[@id="houselist-mod-new"]/li['+ str(i) +']/div[3]/span[1]/strong/text()').extract()[0]
            univalence = tweet_node.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[3]/span[2]/text()').extract()[0]
            location = response1.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[2]/div[3]/span/text()').extract()[0]
            layout = response1.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[2]/div[2]/span[1]/text()').extract()[0]
            size = response1.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[2]/div[2]/span[2]/text()').extract()[0]
            age = 'NA'
            floor = response1.xpath('//*[@id="houselist-mod-new"]/li[' + str(i) + ']/div[2]/div[2]/span[3]/text()').extract()[0]
            city = tweet_node.xpath('//*[@id="switch_apf_id_7"]/span[1]/text()').extract()[0]
            region = location.strip().split('\n')[1].strip()
            address = location.strip().split('\n')[0].strip()

            print(name.strip(), price.strip() + "万", univalence.strip(), city.strip(), region, address, layout.strip(),
                  size.strip(), age.strip(), floor.strip(), sep = '\t')
            i += 1
            
    #fo.close()




if __name__ == '__main__':
    
    url = 'https://sjz.anjuke.com/sale/?from=navigation'
    driver = webdriver.Chrome(chrome_options = chrome_options)
    driver.get(url)
    crawl_house_price()
