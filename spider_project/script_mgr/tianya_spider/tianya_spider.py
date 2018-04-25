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


#天涯论坛爬虫
class TianYaSpider:

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
        params=self.params
        response=requests.get(url,params=params)
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
        for url in url_list:
            spider=MysqlHelper.excuteFindOne("select Fnum from tb_spider where Fid={}".format(self.spiderId))
            num=int(spider["Fnum"])
            num+=1
            #页面源码
            text=self.getHtml(url).text
            #创建一selector,用于xpath去匹配需要的数据
            selector=etree.HTML(text, parser=None, base_url=None)
            #标题
            title=selector.xpath(u'//span[@class="s_title"]/span/text()')
            #发帖人
            p_Fauthor=u"<a href=\".*?\" target=\"_blank\" class=\"js-vip-check\" uid=\".*?\" uname=\".*?\">([\s\S]*?)</a>"
            author=re.findall(p_Fauthor,text)
            #发帖时间
            p_date=u"<span>时间：([\s\S]*?) </span>"
            date=re.findall(p_date,text)
            #内容
            p_content=u"<div class=\"bbs-content clearfix\">([\s\S]*?)</div>"
            content=re.findall(p_content,text)

            data={}
            data["Ftitle"]=title[0] if title else ""
            data["Fdate"]=date[0] if date else "Null"
            data["Fcontent"]=content[0] if content else ""
            data["Flink"]=url
            data["Ftype"]="论坛"
            data["Fsource"]="天涯社区"
            data["FcreateTime"]=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
            data["Fauthor"]=author[0] if author else ""

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
                id=n+b
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
        # print text
        #xpath去匹配需要的数据
        selector=etree.HTML(text, parser=None, base_url=None)
        title_url_list=selector.xpath('//a[@target="_blank"]/@href')
        for x in title_url_list:
            if re.search("/post",x):
                #url过滤去重
                istrue=RedisHelper.urlFilter(x,"tianya_url")
                if istrue==False:
                    url_list.append("http://bbs.tianya.cn"+x)
        return url_list



if __name__ == "__main__":
    try:
        task=MysqlHelper.excuteFindOne("select * from tb_task where Fid={}".format("1002"))
        slave=Slave(task,"tb_spider")
        slave.start()
    except Exception as ex:
        print ex
        MysqlHelper.excuteUpdate("tb_spider",{"Fstate":0},"Fid={}".format("1002"))





