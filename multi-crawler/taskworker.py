# -*- coding:utf-8 -*-
# taskworker.py

import time, sys, Queue
from multiprocessing.managers import BaseManager
from bs4 import BeautifulSoup
import requests,re
import codecs
from urllib import quote, unquote

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
m = QueueManager(address=(server_addr, 5000), authkey='abc')
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:

base_url = "http://baike.baidu.com/item/"
result_file = 'html'

def get_ip():
    import socket
    try:
        csock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        csock.connect(('8.8.8.8', 80))
        (addr, port) = csock.getsockname()
        csock.close()
        return addr
    except socket.error:
        return "127.0.0.1"

workerip = get_ip()
result_file =  workerip +"-html.txt"
fr = codecs.open(result_file, 'a', 'utf-8')

while True:
    try:
        uword = task.get(timeout=1)
        print('run task word=%s...' %uword)
        url = base_url + quote(uword.encode('utf-8'))
        response = requests.get(url)
        content = BeautifulSoup(response.text.encode(response.encoding), 'lxml')

        relate_words = []
        for a in content.find_all('a'):
            if a.attrs.has_key('href'):
                href = a.attrs['href']
                if href.startswith('/item') and not href.endswith('fr=navbar') and not href.endswith('force=1'):
                    word = unquote(href.replace('/item/', '').replace('#viewPageContent', ''))
                    if type(word) == str:
                        word = word.decode('utf-8')
                    relate_words.append(word)

        result.put(r)
    except Queue.Empty:
        print('task queue is empty.')
        time.sleep(10)
# 处理结束:
print('worker exit.')