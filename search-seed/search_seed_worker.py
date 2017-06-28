# -*- coding:utf-8 -*-
# taskworker.py

import time,queue,os,sys
from multiprocessing.managers import BaseManager
from bs4 import BeautifulSoup
import requests, re
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

for i in ['data', 'log']:
    if not os.path.exists(i):
        try:
            os.mkdir(i)
        except:
            print("mkdir %s failed,exit..." % i)
            sys.exit(1)
#获取本机ip
workerip = get_ip()
#获取当前日期
dt = time.strftime('%Y-%m-%d', time.localtime(time.time()))


seed_file = "data/seed%s-%s.txt" % (dt,workerip)
log_file = "log/log%s.txt" % workerip
seed_fw = codecs.open(seed_file, 'a', 'utf-8')
log_fw = codecs.open(log_file, 'a', 'utf-8')

#url
base_url = "http://baike.baidu.com"
search_url = base_url + '/search?word='
item_url = base_url + '/item'
inc = 0
while True:
    #每天生成一个文件
    newdt = time.strftime('%Y-%m-%d',time.localtime(time.time()))
    if newdt != dt:
        seed_fw.close()
        seed_file = "data/seed%s-%s.txt" %(dt,workerip)
        seed_fw = codecs.open(seed_file, 'a', 'utf-8')

    try:
        uword = task.get(timeout=1)
        print('run task word=%s...' % uword)
        url = search_url + quote(uword.encode('utf-8'))

        response = requests.get(url)
        res_text = response.text.encode(response.encoding)

        content = BeautifulSoup(res_text, 'lxml')
        relate_words = []
        for a in content.find_all('a'):
            if 'href' in a.attrs:
                href = a.attrs['href']
                if href.startswith(item_url):
                    word = unquote(href.replace(item_url+'/', ''))
                    relate_words.append(word)
                elif href.startswith('/item'):
                    word = unquote(href.replace('/item/', ''))
                    relate_words.append(word)
        print(len(relate_words))

        seed_fw.write(uword + '\t')
        seed_fw.write(','.join(relate_words))
        seed_fw.write('\n')
        seed_fw.flush()

        for rword in relate_words:
            rword = rword.split('/')[0]
            result.put(rword)

    except queue.Empty:
        print('task queue is empty.')
        time.sleep(10)
    except:
        log_fw.write("bad word:" + word + "\n")
        traceback.print_exc(file=log_fw)
# 处理结束:
print('worker exit.')
