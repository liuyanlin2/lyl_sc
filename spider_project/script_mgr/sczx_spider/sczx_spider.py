#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')
import re
import requests
import time
from lxml import etree
from multiplexing_class.redis_helper import RedisHelper
from multiplexing_class.mysql_helper import MysqlHelper
from multiplexing_class.base_slave import Slave
from script_mgr.negative_keywords import NegativeKeyWords
from elasticsearch import Elasticsearch
from spider_project.settings import ES_HOST,ES_PORT
import random
import datetime

#四川在线和下属论坛爬虫
class SczxSpider:
    """
        :param proxies: 代理ip
        :param params: 携带的访问参数字典类型
        :param pageUrl:打开一个页面里面所有的信息url
        :param spiderId:爬虫id
    """
    def __init__(self,proxies,params,pageUrl,spiderId):
        self.proxies=proxies #代理Ip暂时没用
        self.params=params
        self.pageUrl=pageUrl
        self.spiderId=spiderId
    #获取页面源码
    def getHtml(self,url):
        #代理
        proxies = self.proxies
        params=self.params #因此个网站不能带参数，所以设置为None
        response=requests.get(url,params=params)
        # response.encoding = 'gb2312'
        return response

    #提取数据
    def getItem(self):
        #获取负面关键词
        negative=NegativeKeyWords()
        negKwList=negative.getNegativeKeyWordsList()
        #获取ES搜索引擎数据库连接
        es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
        url_list=self.getPageInfoUrl() #获取页面所有信息的url
        MysqlHelper.excuteUpdate("tb_spider",{"Fstate":1},"Fid={}".format(self.spiderId))
        print len(url_list)
        for url in url_list:
            print url
            spider=MysqlHelper.excuteFindOne("select Fnum from tb_spider where Fid={}".format(self.spiderId))
            num=int(spider["Fnum"])
            num+=1
            print "-----------爬取中---"+str(num)+"---------"
            text=self.getHtml(url).text
            #xpath去匹配需要的数据
            selector=etree.HTML(text, parser=None, base_url=None)
            #标题
            title=selector.xpath('//h1[@class="ts"]//a[@id="thread_subject"]/text()')
            #发表日期
            date=selector.xpath('//em[@class="xg1"]/text()')
            # #发表内容,正则匹配
            content=selector.xpath('//td[@class="t_f"]//text()')
            #来源
            source=selector.xpath('//div[@id="pt"]//div[@class="z"]//a/text()')
            #发帖人
            author=selector.xpath('//div[@class="floor-profile"]//a/text()')


            data={}
            data["Ftitle"]=title[0].encode("utf-8") if title else ""
            Fdate=(date[0]+":00").encode("utf-8").replace("发表于 ","") if date else "Null"
            data["Fdate"]=time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(Fdate,'%Y-%m-%d %H:%M:%S'))
            Fcontent=('').join(content).encode("utf-8") if content else ""
            data["Fcontent"]=Fcontent
            data["Flink"]=url
            data["Ftype"]= "论坛" if re.search(u"论坛",source[2]) else "政务"
            data["Fsource"]= source[2] if source else ""
            data["FcreateTime"]=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            data["Fauthor"]=author[0] if author else ""
            # istrue=MysqlHelper.excuteInsert("tb_data",data)
            #判断是否是负面信息
            def isNegative(key):
                if re.findall(key,data["Fcontent"]):
                    return True
                else:
                    return False
            isNegKeyWor=map(isNegative,negKwList)
            #0正面，1负面
            if True in isNegKeyWor:
                data["isNegative"]=1
            else:
                data["isNegative"]=0

            try:
                n=random.randint(1,9999)
                b=random.randint(1,9999)
                id=n+b+b
                #向ES插入数据  index:索引，相当于mysql的数据库名,doc_type:相当于mysql的表名
                istrue=es.create(index="scdel_index",id=id,doc_type="tb_data",body=data)["created"]
                print istrue
            except Exception as ex:
                print ex
                istrue=False
            if istrue:
                MysqlHelper.excuteUpdate("tb_spider",{"Fnum":num},"Fid={}".format(self.spiderId))
            time.sleep(1)



    #提取每一页面所有信息的url
    def getPageInfoUrl(self):
        url_list=[]
        text=self.getHtml(self.pageUrl).text
        #xpath去匹配需要的数据
        selector=etree.HTML(text, parser=None, base_url=None)
        ulr1=selector.xpath('//th[@class="common"]//a[@class="s xst"]/@href')
        ulr2=selector.xpath('//th[@class="new"]//a[@class="s xst"]/@href')
        title_url_list=ulr1+ulr2
        print len(title_url_list)

        for url in title_url_list:
            num=random.randint(1000,9999)
            # url_list.append(url+"?_dsign="+str(num))
            #url过滤去重
            istrue=RedisHelper.urlFilter(url,"sczx_url")
            if istrue==False:
                # url_list.append(url)
                url_list.append(url+"?_dsign="+str(num))
        return url_list
if __name__ == "__main__":

    try:
        task=MysqlHelper.excuteFindOne("select * from tb_task where Fid={}".format("1005"))
        slave=Slave(task,"tb_spider")
        slave.start()
    except Exception as ex:
        print ex
        MysqlHelper.excuteUpdate("tb_spider",{"Fstate":0},"Fid={}".format("1005"))