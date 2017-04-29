# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import requests, re, time
import codecs
from sougo import *
import traceback
base_url = 'https://shurufa.baidu.com/dict_innerid_download?innerid='
fr = codecs.open('dictinfo.txt','r','utf-8')
for id in fr.readlines():
    row = id.strip().split(',')
    if len(row) != 6:
        continue
    m_id = row[-2]
    print m_id
    url = base_url + m_id
    response = requests.get(url)
    scelfile = "data/"+m_id+".bdict"
    with open(scelfile, "wb") as code:
        code.write(response.content)
    '''
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
    '''



