# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')
import time
from Queue import Queue
from multiprocessing.managers import BaseManager


#从机类
class Slave:

    def __init__(self,task,tablename):
        # 派发出去的任务队列
        self.dispatched_task_queue = Queue()
        # 完成的任务队列
        self.finished_task_queue = Queue()
        self.task=task
        self.tablename=tablename

    def start(self):
        # 把派发任务队列和完成任务队列注册到网络上
        BaseManager.register('get_dispatched_task_queue')
        BaseManager.register('get_finished_task_queue')

        # 连接master
        server =self.task["FserverIp"]  # 如'192.168.1.102'
        port=self.task["Fport"]
        authkey=self.task["Fauthkey"]
        # print('连接主机服务器 %s...' % server)
        manager = BaseManager(address=(server,int(port)), authkey=authkey)
        manager.connect()

        # 使用上面注册的方法获取队列
        dispatched_tasks = manager.get_dispatched_task_queue()
        finished_tasks = manager.get_finished_task_queue()

        # 运行作业并返回结果
        while True:
            try:
                spider = dispatched_tasks.get(timeout=1)
                spider.getItem()
                time.sleep(1)
                finished_tasks.put(spider)
            except Exception as ex:
                # raise Exception(ex)
                continue
