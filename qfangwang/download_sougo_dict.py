# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, re, time
import codecs
from sougo import *
import traceback
payload = {}
headers = {'Host': 'wubi.sogou.com',
           'Origin': 'http://wubi.sogou.com',
           'Referer': 'http://wubi.sogou.com/dict/',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.98 Safari/537.36'}

fr = codecs.open('dictinfo.txt','r','utf-8')
for id in fr.readlines():
    row = id.strip().split(',')
    url = row[2]
    m_id = row[1]
    print url, m_id
    response = requests.get(url)
    scelfile = "data/"+m_id+".scel"
    with open(scelfile, "wb") as code:
        code.write(response.content)
    try:
        generator = get_word_from_sogou_cell_dict(scelfile)
        #showtxt(generator)
        txtfile = "txtdata/" + m_id + ".txt"
        writefile(generator,txtfile)
        time.sleep(1)
    except:
        logfw = open('trace-download.txt', 'a')
        traceback.print_exc(file=logfw)
        logfw.write("m_id:" + m_id+'\n')
        logfw.flush()
        logfw.close()



