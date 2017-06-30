import time, sys, queue,os
from multiprocessing.managers import BaseManager
from bs4 import BeautifulSoup
import requests
import codecs
from urllib.parse import quote, unquote
import traceback
import config
def crawler_data(url):
    response = requests.get(url)
    res_text = response.text.encode(response.encoding)
    content = BeautifulSoup(res_text, 'lxml')
    url1 = "https://baike.baidu.com"

    relate_words = []
    for a in content.find_all('a'):
        if 'href' in a.attrs:
            href = a.attrs['href']
            if href.find('/item') > -1 and not href.endswith('fr=navbar') and \
                not href.endswith('force=1') and \
                    href.find('/mall/item?id=') == -1:
                filterList = [url, url1, '/item/', '#viewPageContent', '#hotspotmining']
                for fstr in filterList:
                    href = href.replace(fstr, '')
                word = unquote(href)
                relate_words.append(word)
    return set(relate_words)

if __name__ == '__main__':
    url = "http://baike.baidu.com"
    for i in crawler_data(url):
        print(i)