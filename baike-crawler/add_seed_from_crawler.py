# -*- coding:utf-8 -*-

#从某些动态页面动态的获取种子

import time, sys, queue,os
from multiprocessing.managers import BaseManager
from bs4 import BeautifulSoup
import requests
import codecs
from urllib.parse import quote, unquote
import traceback
import config

# 创建类似的QueueManager:
class QueueManager(BaseManager):
    pass


# 由于这个QueueManager只从网络上获取Queue，所以注册时只提供名字:
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')

# 连接到服务器，也就是运行taskmanager.py的机器:

print('Connect to server %s...' % config.server_addr)
# 端口和验证码注意保持与taskmanager.py设置的完全一致:
m = QueueManager(address=(config.server_addr, config.port), authkey=config.passwd.encode('utf-8'))
# 从网络连接:
m.connect()
# 获取Queue的对象:
task = m.get_task_queue()
result = m.get_result_queue()
# 从task队列取任务,并把结果写入result队列:

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

for i in ['seed-data', 'log']:
    if not os.path.exists(i):
        try:
            os.mkdir(i)
        except:
            print("mkdir %s failed,exit..." % i)
            sys.exit(1)

# 获取本机ip
workerip = get_ip()
# 获取当前日期
dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))

inc = 0
seed_file = "seed-data/seed%s-%s_%d.txt" % (dt, workerip,inc/1000)
log_file = "log/seedlog%s.txt" % workerip
fw = codecs.open(seed_file, 'a', 'utf-8')
log_fw = codecs.open(log_file, 'a', 'utf-8')

url = "http://baike.baidu.com"
url1 = "https://baike.baidu.com"

filterList = [url, url1, '/item/', '#viewPageContent', '#hotspotmining']
while True:
    # 每天生成一个文件
    inc += 1
    if inc % 10001 == 0:
        newdt = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        if newdt != dt:
            inc = 0
            dt = newdt
        fw.close()
        seed_file = "seed-data/seed%s-%s_%d.txt" % (dt, workerip, inc/1000)
        fw = codecs.open(seed_file, 'a', 'utf-8')

    try:
        response = requests.get(url)
        res_text = response.text.encode(response.encoding)
        content = BeautifulSoup(res_text, 'lxml')

        relate_words = set()
        for a in content.find_all('a'):
            if 'href' in a.attrs:
                href = a.attrs['href']
                if href.find('/item') > -1 and not href.endswith('fr=navbar') and \
                        not href.endswith('force=1') and \
                        href.find('/mall/item?id=') == -1:

                    for fstr in filterList:
                        href = href.replace(fstr, '')
                    word = unquote(href)
                    relate_words.add(word)
        # print(len(relate_words))
        for w in relate_words:
            result.put(w)

        fw.write("\n".join(relate_words) + "\n")
        fw.flush()
    except queue.Empty:
        print('task queue is empty.')
        time.sleep(10)
    except:
        traceback.print_exc(file=log_fw)
    time.sleep(300)
# 处理结束:
print('worker exit.')
