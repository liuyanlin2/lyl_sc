# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')
from multiprocessing.managers import BaseManager
from multiprocessing import Queue
import time
from mysql_helper import MysqlHelper

#主机任务派发管理类，用于任务派发
class Master:

    """
        :param url_list:获取要爬取的url类，用于任务派发
        :param spider:爬虫类
        :param taskId:任务id
        :param table_name:表名
    """
    def __init__(self,url_list,spider,taskId,table_name):
        # 派发出去的任务队列
        self.dispatched_task_queue = Queue()
        # 完成的任务队列
        self.finished_task_queue = Queue()
        self.url_list=url_list
        self.spider=spider
        self.taskId=taskId
        self.table_name=table_name

    def get_dispatched_task_queue(self):
        return self.dispatched_task_queue

    def get_finished_task_queue(self):
        return self.finished_task_queue


    #开始任务
    def start(self):
        # 把派发作业队列和完成作业队列注册到网络上
        BaseManager.register('get_dispatched_task_queue', callable=self.get_dispatched_task_queue)
        BaseManager.register('get_finished_task_queue', callable=self.get_finished_task_queue)

        task=MysqlHelper.excuteFindOne("select * from tb_task where Fid={}".format(self.taskId))
        Fip=task["FserverIp"]
        Fport=task["Fport"]
        Fauthkey=task["Fauthkey"]
        # 监听端口和启动服务，Fauthkey为验证码，自己随便取的,slave连接获取任务时用于验证身份，FserverIp为主机的ip,Fport连接端口号，一般默认是8888端口
        manager = BaseManager(address=(Fip, Fport), authkey=Fauthkey)
        manager.start()

        # 使用上面注册的方法获取队列
        dispatched_tasks = manager.get_dispatched_task_queue() #获取派发队列
        finished_tasks = manager.get_finished_task_queue() #获取返回队列


        while True:
            try:
                task_2=MysqlHelper.excuteFindOne("select * from tb_task where Fid={}".format(self.taskId))
                num=int(task_2["Fnum"])
                url_list=self.url_list
                for index,url in enumerate(url_list):
                    print url
                    num+=1
                    dispatched_spider=self.spider
                    dispatched_spider.pageUrl=url
                    dispatched_tasks.put(dispatched_spider)
                    print "派发任务： "+str(index+1)
                    MysqlHelper.excuteUpdate(self.table_name,{"Fnum":str(num+1),"Fstate":1},"Fid={}".format(self.taskId))
                    time.sleep(1)
                print "------------已完成一轮任务派发----------"
                #完成一轮任务派发就将状态改为休眠中
                MysqlHelper.excuteUpdate(self.table_name,{"Fstate":2},"Fid={}".format(self.taskId))
                #返回队列执行结果
                while not dispatched_tasks.empty():
                    #返回一个爬取的数量结果
                    result_spider = finished_tasks.get()
                    print "任务返回结果："
                #暂停时间继续进行下一轮的任务派发
                # time.sleep(int(task_2["FtimeInterval"]))
                manager.shutdown()
            except Exception as ex:
                MysqlHelper.excuteUpdate(self.table_name,{"Fstate":0},"Fid={}".format(self.taskId))
                continue


