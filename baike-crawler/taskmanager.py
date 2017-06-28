# -*- coding:utf-8 -*-

import time, queue, codecs, sys
from multiprocessing.managers import BaseManager
import config
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

manager = QueueManager(address=('', config.port), authkey=config.passwd.encode('utf-8'))
# 启动Queue:
manager.start()
# 获得通过网络访问的Queue对象:
task = manager.get_task_queue()
result = manager.get_result_queue()

# 每次重启时载入已完成的种子
finished_file = sys.argv[1]
finished_set = set()

with codecs.open(finished_file, 'r', 'utf-8') as f:
    finished_set.update([i.strip() for i in f.readlines() if len(i.strip()) != 0])

while True:
    try:
        r = result.get(timeout=10)
        if r not in finished_set:
            task.put(r)
            finished_set.add(r)
    except queue.Empty:
        print('Queue is empty')
        time.sleep(10)
# 关闭:
manager.shutdown()
