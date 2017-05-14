# -*- coding:utf-8 -*-

a = '''<span class="taglist">
<a target="_blank" href="/wikitag/taglist?tagId=64469">股票名称</a>
</span>'''

import time, sys, queue
from multiprocessing.managers import BaseManager
from bs4 import BeautifulSoup
import requests,re
import codecs
from urllib.parse import quote, unquote
import traceback

content = BeautifulSoup(a, 'lxml')
print(content.select('a')[0].string)
