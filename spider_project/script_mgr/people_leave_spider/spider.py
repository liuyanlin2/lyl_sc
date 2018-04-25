#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')
import re
import requests
import time
from lxml import etree
from multiplexing_class.redis_helper import RedisHelper
from script_mgr.negative_keywords import NegativeKeyWords
import random
import datetime
from multiplexing_class.save_data import SaveData
from multiplexing_class.utility_class import Utility

#人民网《地方领导留言板》爬虫
class PeopleSpider:

    """
        :param proxies_list: 代理ip列表
        :param params_list: 携带的访问参数列表
        :param pageUrl:打开一个页面里面所有的信息url（这里是每个地方论坛首页的url）
        :param port:端口号
        :param authkey:验证码
    """
    def __init__(self,proxies_list=None,params_list=None,pageUrl=None):
        self.proxies_list=proxies_list
        self.params_list=params_list
        self.pageUrl=pageUrl
        self.port=8882
        self.authkey='people'

    #获取页面源码
    def getHtml(self,url):
        #代理，代理Ip暂时没用
        proxies = random.choice(self.proxies_list) #随机获取一个代理Ip
        params=random.choice(self.params_list) #随机获取一个携带的User-Agent参数
        response=requests.get(url,params=params)
        return response
    #提取数据
    def getItem(self):
        try:
            #获取负面关键词
            negative=NegativeKeyWords()
            negKwList=negative.getNegativeKeyWordsList()
            url_list=self.getPageInfoUrl() #获取页面所有信息的url
            data_list=[] #爬取的数据
            for url in url_list:
                #页面源码
                text=self.getHtml(url).text
                #创建一selector,用于xpath去匹配需要的数据
                selector=etree.HTML(text, parser=None, base_url=None)
                #标题
                title=selector.xpath('//h2/b/text()')
                #发表日期
                date=selector.xpath('//h3[@class="fl grey2 clearfix"]/span/text()')
                #发表内容,正则匹配
                content=selector.xpath('//p[@id="zoom"]//text()')

                data={}
                data["Ftitle"]=title[0].encode("utf-8") if title else ""
                Fdate=(re.findall(r"\d{4}-\d+-\d+ \d{2}:\d+",date[0])[0]+":00") if date else "Null"
                data["Fdate"]=time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(Fdate,'%Y-%m-%d %H:%M:%S'))
                Fcontent=content[0].encode("utf-8") if content else ""
                data["Fcontent"]=Fcontent
                data["Flink"]=url
                data["Ftype"]="政务"
                data["Fsource"]="人民网《地方领导留言板》"
                data["FcreateTime"]=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                data["Fauthor"]=date[0].replace(re.findall(r"\d{4}-\d+-\d+ \d{2}:\d+",date[0])[0],"") if date else ""
                print "-------------------------"
                print data["Ftitle"]
                print data["Fdate"]


                #为保证所获取到到数据是最新的，所以判断信息发表日期是否属于当前日期，如果不是则跳过不保存
                # if Utility().getCurrentDate()==str(datetime.datetime.strptime(Fdate, "%Y-%m-%d")):
                #     #判断是否是负面信息
                #     def isNegative(key):
                #         if re.findall(key,data["Fcontent"]):
                #             return True
                #         else:
                #             return False
                #     isNegKeyWor=map(isNegative,negKwList)
                #     #0正面，1负面
                #     data["isNegative"]=1 if True in isNegKeyWor else 0
                #     data_list.append(data)
            #保存数据
            # save=SaveData('人民网《地方领导留言板》',data_list)
            # save.saveDataBatch()
        except Exception as ex:
            print ex

    #提取每一页面所有信息的url
    def getPageInfoUrl(self):
        url_list=[]
        text=self.getHtml(self.pageUrl).text
        print text
        #xpath去匹配需要的数据
        selector=etree.HTML(text, parser=None, base_url=None)
        title_url_list=selector.xpath('//h2//b//a/@href')
        for url in title_url_list:
            print "http://liuyan.people.com.cn/"+url
            url_list.append("http://liuyan.people.com.cn/"+url)

            # #url过滤去重
            # istrue=RedisHelper.urlFilter("http://liuyan.people.com.cn/"+url,"people_url")
            # if istrue==False:
            #     url_list.append("http://liuyan.people.com.cn/"+url)
        return url_list









