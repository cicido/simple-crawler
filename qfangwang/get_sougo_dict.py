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

import traceback

fw = codecs.open('dictinfo-unfinished.txt', 'w', 'utf-8')
fr = open('class-unfinished.txt')
for id in fr.readlines():
    try:
        cat = id.strip().split(',')[-1]
        print cat
        url = base_url + param + cat
        response = requests.get(url, data=payload, headers=headers)
        content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')
        pagenum = int(content.find('div', class_='pagenavi').find('span', class_='num').string)
        print pagenum

        for page in range(1, pagenum + 1):
            pageurl = url + "&page=%d" % page
            print pageurl
            response = requests.get(pageurl, data=payload, headers=headers)
            content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')
            for dictbox in content.find_all('div', class_='dictbox'):
                m_href = dictbox.div.div.a.attrs.get('href')
                m_id = dictbox.h2.a.attrs.get('href').split('=')[1]
                m_name = dictbox.h2.a.string
                m_ul = dictbox.ul.find_all('li')
                m_detail = m_ul[1].string.replace('&nbsp', '')
                m_time = m_ul[2].string
                print ','.join([cat, m_id, m_href, m_name, m_detail, m_time])
                fw.write(','.join([cat, m_id, m_href, m_name, m_detail, m_time]) + '\n')

                '''
                r = requests.get(m_href)
                with open("data/"+m_id+".scel", "wb") as code:
                    code.write(r.content)
                '''
            time.sleep(1)
    except:
        logfw = open('trace.txt', 'a')
        traceback.print_exc(file=logfw)
        logfw.write(id)
        logfw.flush()
        logfw.close()

fw.close()
