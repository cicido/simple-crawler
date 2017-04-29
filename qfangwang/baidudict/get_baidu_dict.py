# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, re, time
import codecs

base_url = "https://shurufa.baidu.com/dict"
param = '_list?cid='

import traceback

fw = codecs.open('dictinfo.txt', 'w', 'utf-8')
fr = open('class.txt','r')
for id in fr.readlines():
        cat = id.strip().split(',')[1]
        print cat
        url = base_url + param + cat
        response = requests.get(url)
        content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')
        #print content.find('div', class_='pages tc').find('input', id='target').attrs
        #<div class="pages tc">
        pagenum = 1
        try:
            pagenum = int(content.find('div', class_='pages tc').find('input', id='target').attrs.get('maxpage'))
        except:
            logfw = open('trace.txt', 'a')
            traceback.print_exc(file=logfw)
            logfw.write(id)
            logfw.flush()
            logfw.close()

        print pagenum
        if pagenum != 1:
            continue
        for page in range(1, pagenum + 1):
            pageurl = url + "&page=%d" % page
            print pageurl,page
            response = requests.get(pageurl)
            content = BeautifulSoup(response.text, 'lxml')
            #<div class="dict-list-info">
            dictlist = content.find('div', class_='dict-list-info')
            for dictbox in dictlist.find_all('a',class_="dict-down dictClick"):
                m_innerid = dictbox.attrs.get('dict-innerid')
                m_dictname = dictbox.attrs.get('dict-name')
                #print id,m_innerid,m_dictname
                fw.write(','.join([id.strip(),m_innerid,m_dictname.encode('utf-8')]).decode("utf-8") + '\n')
                fw.flush()
            #time.sleep(1)

fw.close()

