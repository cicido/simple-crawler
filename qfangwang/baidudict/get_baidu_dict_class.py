# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, re, time
import codecs

base_url = "https://shurufa.baidu.com/dict"

response = requests.get(base_url)

# 保存层次关系
classmap = {}

content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')
classwr = codecs.open('class.txt','w','utf-8')
#<ul class='list_contain'>
ul = content.find('div', class_='dict_category clearfix').ul
#print ul
for li in ul.find_all('li'):
    cat1_id = li.a.attrs.get('href').split('=')[1]
    cat1_name = li.find_all('span')[1].string
    #print cat1_id, cat1_name

    div = li.find('div',class_ = 'sort-tag')
    for cat2 in div.find_all('a'):
        cat2_id = cat2.attrs.get('href').split('=')[1]
        cat2_name = cat2.string.strip()
        print cat1_id,cat2_id,cat1_name,cat2_name
        classwr.write(','.join([cat1_id,cat2_id,cat1_name,cat2_name]) + '\n')
classwr.close()