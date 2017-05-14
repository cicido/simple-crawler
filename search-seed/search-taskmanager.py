# -*- coding:utf-8 -*-

# taskmanager.py

import random, time, queue,codecs
from multiprocessing.managers import BaseManager

# 发送任务的队列:
task_queue = queue.Queue()
# 接收结果的队列:
result_queue = queue.Queue()

# 从BaseManager继承的QueueManager:
class QueueManager(BaseManager):
    pass

# 把两个Queue都注册到网络上, callable参数关联了Queue对象:
QueueManager.register('get_task_queue', callable=lambda: task_queue)
QueueManager.register('get_result_queue', callable=lambda: result_queue)
# 绑定端口5000, 设置验证码'abc':
manager = QueueManager(address=('', 5000), authkey='abc'.encode('utf-8'))
# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()

# 已完成与未完成的词条文件，每次重启前更新这两个文件
finished_file = 'word-finished.txt'
unfinished_file = 'word-unfinished.txt'

finished_set = set()
unfinished_set = set()

with codecs.open(finished_file, 'r', 'utf-8') as f:
    finished_set.update([i.strip() for i in f.readlines() if len(i.strip()) != 0])

with codecs.open(unfinished_file, 'r', 'utf-8') as f:
    unfinished_set.update([i.strip() for i in f.readlines() if len(i.strip()) != 0])

# 种子任务
for i in unfinished_set:
    task.put(i)
finished_set.update(unfinished_set)

while True:
    try:
        r = result.get(timeout=10)
        if r not in finished_set:
            print('new word: %s' % r)
            task.put(r)
            finished_set.add(r)
    except queue.Empty:
        print('Queue is empty')
        time.sleep(10)
# 关闭:
manager.shutdown()
