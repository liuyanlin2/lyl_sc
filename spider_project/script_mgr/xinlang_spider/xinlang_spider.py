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
from multiplexing_class.save_data import SaveData

#新浪论坛爬虫
class XinLangSpider:
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
        response.encoding = 'gb2312'
        return response

    #提取数据
    def getItem(self):
        #获取负面关键词
        negative=NegativeKeyWords()
        negKwList=negative.getNegativeKeyWordsList()
        url_list=self.getPageInfoUrl() #获取页面所有信息的url
        # data_list=[] #爬取的数据
        for url in url_list:
            try:
                print "爬取中-------"
                text=self.getHtml(url).text
                #xpath去匹配需要的数据
                selector=etree.HTML(text, parser=None, base_url=None)
                #标题
                title=selector.xpath('//h1/span/text()')
                #发表日期
                p_date=u"<font color=\"#c5c5c5\">发表于：([\s\S]*?)</font>"
                date=re.findall(p_date,text)
                #发表内容,正则匹配
                content=selector.xpath('//div[@class="mybbs_cont"]//text()')
                #发帖人
                p_Fauthor=u"<a href=\".*?\" target=\"_blank\" class=\"f14\">([\s\S]*?)</a>"
                author=re.findall(p_Fauthor,text)

                data={}
                data["Ftitle"]=title[0].encode("utf-8") if title else ""
                Fdate=(date[0]+":00").encode("utf-8").replace("发表于 ","") if date else "Null"
                data["Fdate"]=time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(Fdate,'%Y-%m-%d %H:%M:%S'))
                Fcontent=('').join(content).encode("utf-8") if content else ""
                data["Fcontent"]=Fcontent
                data["Flink"]=url
                data["Ftype"]="论坛"
                data["Fsource"]="新浪杂谈"
                data["FcreateTime"]=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
                data["Fauthor"]=author[0].encode("utf-8") if author else ""
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
                print data

                s=SaveData('新浪杂谈')
                istue=s.saveData(data)
                print istue

                # data_list.append(data)
                # time.sleep(1)
                # #保存数据
                # s=SaveData(data_list,'新浪杂谈')
                # s.saveData()
            except Exception as ex:
                continue

    #提取每一页面所有信息的url
    def getPageInfoUrl(self):
        url_list=[]
        text=self.getHtml(self.pageUrl).text
        #xpath去匹配需要的数据
        selector=etree.HTML(text, parser=None, base_url=None)
        title_url_list=[]
        title_url_list+=selector.xpath('//th[@class="new"]//a[@target="_blank"]/@href')
        title_url_list+=selector.xpath('//th[@class="hot"]//a[@target="_blank"]/@href')
        title_url_list+=selector.xpath('//th[@class="common"]//a[@target="_blank"]/@href')
        for x in title_url_list:
            url="http://club.history.sina.com.cn/"+x
            url_list.append(url)
            # #url过滤去重
            # istrue=RedisHelper.urlFilter(url,"xinlang_url")
            # if istrue==False:
            #     url_list.append(url)
        return url_list
if __name__ == "__main__":

    try:
        task=MysqlHelper.excuteFindOne("select * from tb_task where Fid={}".format("1003"))
        slave=Slave(task,"tb_spider")
        slave.start()
    except Exception as ex:
        print ex
        MysqlHelper.excuteUpdate("tb_spider",{"Fstate":0},"Fid={}".format("1003"))