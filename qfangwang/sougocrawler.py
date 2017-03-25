# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, re, time
import codecs

base_url = "http://wubi.sogou.com/dict/"

payload = {}
headers = {'Host': 'wubi.sogou.com',
           'Origin': 'http://wubi.sogou.com',
           'Referer': 'http://wubi.sogou.com/dict/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}
classmap = {}

response = requests.post(base_url, data=payload, headers=headers)
print type(response)
print type(response.content)
print response.encoding
print response.apparent_encoding
content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')
# <table class="dictcate">
main_table = content.find('table', class_='dictcate')
main_label = []
for label in main_table.find_all('h2'):
    m_href = label.a.attrs.get('href')
    m_text = label.a.string
    main_label.append((m_href, m_text))
    print m_href, m_text
print main_label[0][1]

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
