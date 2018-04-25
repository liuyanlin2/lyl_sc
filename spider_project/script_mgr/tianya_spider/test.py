# -*- coding: utf-8 -*-

from tianya_url import TianYaUrl
from multiplexing_class.mysql_helper import MysqlHelper
from multiplexing_class.redis_helper import RedisHelper
from tianya_spider import TianYaSpider


# keywords_list=MysqlHelper.excuteFindAll("select FkeyWord from tb_keywords")
# print keywords_list
# tianya=TianYaUrl("tianya_url.txt",3,keywords_list)
# url_list=tianya.getUrlAll()
# for url in url_list:
#     print url

# RedisHelper.insertListData("tianya_url","/post-free-5705844-1.shtml")


# proxies = { "http": "http://115.220.3.253:808", "https": "http://121.31.147.192:8123", }
# params={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"}
# url="http://bbs.tianya.cn/list.jsp?item=63&order=1&nextid=0&k=贪腐"
# tianya_spider=TianYaSpider(proxies,params,url,"192.168.0.102")
# # list=tianya_spider.getPageInfoUrl()
# # print len(list)
# # for url in list:
# #     print url
# tianya_spider.getItem()
import re
import requests
import time
from lxml import etree



response=requests.get("http://club.history.sina.com.cn/thread-7605378-1-1.html")
response.encoding = 'gb2312'
text=response.text

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
data["Flink"]=""
data["Ftype"]="论坛"
data["Fsource"]="新浪论坛"
data["FcreateTime"]=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
data["Fauthor"]=author[0].encode("utf-8") if author else ""

print data["Ftitle"]
print data["Fdate"]
print data["Fcontent"]
print data["Flink"]
print data["Ftype"]
print data["Fsource"]
print data["FcreateTime"]
print data["Fauthor"]
# istrue=MysqlHelper.excuteInsert("tb_data",data)
# print istrue


