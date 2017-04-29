# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, re, time
import codecs

base_url = "http://wubi.sogou.com/dict/"
param = 'list.php?c='

payload = {}
headers = {'Host': 'wubi.sogou.com',
           'Origin': 'http://wubi.sogou.com',
           'Referer': 'http://wubi.sogou.com/dict/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}

response = requests.post(base_url, data=payload, headers=headers)
# print type(response)
# print type(response.content)
# print response.encoding
# print response.apparent_encoding

# labledict 保存id与label值对应关系
labeldict = {}

# 保存层次关系
classmap = {}

content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')
# <table class="dictcate">

labelwr = codecs.open("id2label.txt",'w','utf-8')
classwr = codecs.open('class.txt','w','utf-8')
main_table = content.find('table', class_='dictcate')
for label in main_table.find_all('h2'):
    m_href = label.a.attrs.get('href').split('=')[1]
    m_text = label.a.string
    print m_href, m_text
    labelwr.write(m_href+"="+m_text+'\n')
    classmap[m_href] = {}

for id in classmap.keys():
    url = base_url + param + id
    #print url
    response = requests.post(url, data=payload, headers=headers)
    content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')
    # <table class ="catelist" >
    sec_table = content.find('table', class_='catelist')
    for sec in sec_table.find_all('a'):
        m_href = sec.attrs.get('href').split('=')[1]
        m_text = sec.string
        labelwr.write(m_href+"="+m_text+'\n')
        classmap[id][m_href] = {}
        print id, m_href, m_text

for id in classmap.keys():
    for sec in classmap[id].keys():
        url = base_url + param + sec
        response = requests.post(url, data=payload, headers=headers)
        content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')
        third_table = content.find_all('table',class_ = 'catelist')
        if len(third_table) > 1:
            for third in third_table[1].find_all('a'):
                m_href = third.attrs.get('href').split('=')[1]
                m_text = third.string
                labelwr.write(m_href+"="+m_text+'\n')
                classmap[id][sec][m_href] = {}
                print id,sec,m_href
                classwr.write(id + ","+ sec + ","+ m_href + "\n")
        else:
            classwr.write(id + "," + sec + '\n')

labelwr.close()
classwr.close()







'''
for fclass in firstClass:
    url = base_url + fclass
    response = requests.post(url, data=payload, headers=headers)
    content = BeautifulSoup(response.text,'lxml')
    tb = content.find('table', class_='cate_words_list')
    print url
    for sec in tb.find_all('div', class_='cate_no_child', recursive=True, limit=3):
        print sec.a.attrs.get('href'), sec.a.string



url = 'http://pinyin.sogou.com/dict/cate/index/1'
payload = {}
headers = {'Host': 'pinyin.sogou.com',
           'Origin': 'http://pinyin.sogou.com',
           'Referer': 'http://pinyin.sogou.com/dict',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
response = requests.post(url, data=payload, headers=headers)
print response.text
with codecs.open('test.html','w',encoding='utf8') as wr:
    wr.write(response.text)


with open('test.html','wb') as wr:
    wr.write(response.read)
content = BeautifulSoup(response.text, 'lxml')

nav = content.find(id='dict_nav_list')
for first_class in nav.find_all('a'):
    print first_class.attrs.get('href')
'''
