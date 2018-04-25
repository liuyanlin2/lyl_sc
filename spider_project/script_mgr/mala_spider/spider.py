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
import datetime
from multiplexing_class.save_data import SaveData
import random
from multiplexing_class.utility_class import Utility

#四川麻辣论坛爬虫,给定文章url爬取文章内容
class MaLaSpider:

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
        self.port=8881
        self.authkey='mala'


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
                text=self.getHtml(url).text
                p_content="<td class=\"t_f\" id=\".*?\">([\s\S]*?)</td>"
                #xpath去匹配需要的数据
                selector=etree.HTML(text, parser=None, base_url=None)
                #标题
                title=selector.xpath('//h1[@class="ts"]/span[@id="thread_subject" and @style="display:none"]/text()')
                #发表日期
                date=selector.xpath('//div[@class="authi"]/em/text()')
                #发表内容,正则匹配
                content=re.findall(p_content,text)
                #发帖人/机构
                p_Fauthor=u"<a href=\".*?\" target=\"_blank\" class=\"xw1\">([\s\S]*?)</a>"
                author=re.findall(p_Fauthor,text)

                data={}
                data["Ftitle"]=title[0].encode("utf-8") if title else ""
                Fdate=(date[0]+":00").encode("utf-8").replace("发表于 ","") if date else "Null"
                data["Fdate"]=datetime.datetime.strptime(Fdate, "%Y-%m-%d %H:%M:%S")
                dr = re.compile(r'<[^>]+>',re.S)
                Fcontent=content[0] if content else ""
                data["Fcontent"]=dr.sub('',Fcontent).encode("utf-8")
                data["Flink"]=url
                data["Ftype"]="论坛"
                data["Fsource"]="四川麻辣社区"
                data["FcreateTime"]=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                data["Fauthor"]=author[0].encode("utf-8") if author else ""
                print "------------------"
                print data["Ftitle"]
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
            # save=SaveData('四川麻辣社区',data_list)
            # save.saveDataBatch()
        except Exception as ex:
            pass

    #提取每一页面所有信息的url
    def getPageInfoUrl(self):
        url_list=[]
        text=self.getHtml(self.pageUrl).text
        #xpath去匹配需要的数据
        selector=etree.HTML(text, parser=None, base_url=None)
        title_url_list=selector.xpath('//a[@class="s xst" and @onclick="atarget(this)"]/@href')
        for url in title_url_list:
            url_list.append(url)
            print url
            #url过滤去重
            # istrue=RedisHelper.urlFilter(url,"mala_url")
            # if istrue==False:
            #     url_list.append(url)
        return url_list











