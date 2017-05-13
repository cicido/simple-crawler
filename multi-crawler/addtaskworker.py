# -*- coding:utf-8 -*-
# taskworker.py

import time, sys, queue
from multiprocessing.managers import BaseManager
from bs4 import BeautifulSoup
import requests,re
import codecs
from urllib.parse import quote, unquote
import traceback

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass

# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行taskmanager.py的机器:
server_addr = '172.17.32.220'
print('Connect to server %s...' % server_addr)
# 端口和验证码注意保持与taskmanager.py设置的完全一致:
m = QueueManager(address=(server_addr, 5000), authkey='abc'.encode('utf-8'))
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:

unfinished_file = 'word-unfinished.txt'
unfinished_set = set()
with codecs.open(unfinished_file, 'r', 'utf-8') as f:
    unfinished_set.update([i.strip() for i in f.readlines() if len(i.strip()) != 0])

for w in unfinished_set:
    result.put(w)

# 处理结束:
print('worker exit.')
