#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')
import smtplib
from email.mime.text import MIMEText
import random
from multiprocessing.managers import BaseManager
from multiprocessing import Queue
import time
from time import strftime,gmtime
#常用工具类方法封装
class Utility:

    """
        发送qq邮件
        :param sendEmail: 发送者邮箱
        :param recEmail: 接收者邮箱
        :param pwd:IMAP/SMTP服务授权码，在qq邮箱中，找到设置，选择账户，在里面找到IMAP/SMTP服务服务，点击开启，获取授权码
        :param subject: 邮件主题
        :param recEmail: 发送内容
    """
    @staticmethod
    def sendEmail(sendEmail,recEmail,pwd,subject,msg):
        msg= MIMEText(msg) #邮件发送内容
        msg["Subject"]=subject
        msg["From"]=sendEmail
        msg["To"]=recEmail
        try:
            s = smtplib.SMTP_SSL("smtp.qq.com", 465)
            s.login(sendEmail, pwd)
            s.sendmail(sendEmail, recEmail, msg.as_string())
            s.quit()
            print "Success!"
        except smtplib.SMTPException,e:
            pass

    """
     获取唯一int类型的Id
   """
    @staticmethod
    def getId():
        n=random.randint(1,9999999)
        b=random.randint(1,9999999)
        id=n+b+n
        return id

    '''
        获取当期日期
    '''
    @staticmethod
    def getCurrentDate():
        return str(strftime("%Y-%m-%d", gmtime()))

#----------------多进程任务执行封装----------------------------
#主机任务派发管理类，用于任务派发
class Master:

    """
        :param url_list:url列表，用于任务派发
        :param spider:爬虫
    """
    def __init__(self,url_list,spider):
        # 派发出去的任务队列
        self.distribute_queue = Queue()
        # 完成返回的任务队列
        self.return_queue = Queue()
        self.url_list=url_list
        self.spider=spider


    def get_distribute_queue(self):
        return self.distribute_queue

    def get_return_queue(self):
        return self.return_queue


    #开始任务
    def start(self):
        # 把派发作业队列和完成作业队列注册到网络上
        BaseManager.register('get_distribute_queue', callable=self.get_distribute_queue)
        BaseManager.register('get_return_queue', callable=self.get_return_queue)

        # 监听端口和启动服务，Fauthkey为验证码，自己随便取的,slave连接获取任务时用于验证身份，FserverIp为主机的ip,Fport连接端口号，一般默认是8888端口
        manager = BaseManager(address=('127.0.0.1',self.spider.port), authkey=self.spider.authkey)
        manager.start()

        # 使用上面注册的方法获取队列
        distribute_queue = manager.get_distribute_queue() #获取派发队列
        return_queue = manager.get_return_queue() #获取返回队列


        while True:
            try:
                for index,url in enumerate(self.url_list):
                    self.spider.pageUrl=url
                    distribute_queue.put(self.spider)
                    print "派发任务编号： "+str(index+1)
                print "------------已完成一轮任务派发----------"

                #返回队列执行结果
                while not distribute_queue.empty():
                    #返回一个爬取的数量结果
                    result = return_queue.get()
                    print "任务返回结果：",result
                #暂停时间继续进行下一轮的任务派发
                # time.sleep(int(task_2["FtimeInterval"]))
                manager.shutdown()
            except Exception as ex:
                print ex
                continue
            time.sleep(180)



#从机类,接收Master主机派发的任务并执行，返回结果
class Slave:

    def __init__(self,spider):
        # 派发出去的任务队列
        self.distribute_queue = Queue()
        # 完成的任务队列
        self.return_queue = Queue()
        self.spider=spider


    def start(self):
        # 把派发任务队列和完成任务队列注册到网络上
        BaseManager.register('get_distribute_queue')
        BaseManager.register('get_return_queue')

        # 连接master
        # print('连接主机服务器 %s...' % server)
        manager = BaseManager(address=('127.0.0.1',self.spider.port), authkey=self.spider.authkey)
        manager.connect()

        # 使用上面注册的方法获取队列
        distribute_queue = manager.get_distribute_queue()
        return_queue = manager.get_return_queue()

        # 运行作业并返回结果
        while True:
            try:
                spider = distribute_queue.get(timeout=1)
                spider.getItem()
                time.sleep(1)
                return_queue.put(True)
            except Exception as ex:
                # raise Exception(ex)
                return_queue.put(False)
                continue

