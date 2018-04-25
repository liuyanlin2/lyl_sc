# -*- coding: utf-8 -*-
import xlrd
from xlwt import *
#------------------读数据---------------------------------
# fileName='C:\Users\st\Desktop\HelloWorld\weburl.xlsx'
# bk=xlrd.open_workbook(fileName)
# shxrange=range(bk.nsheets)
# try:
#     sh=bk.sheet_by_name("Sheet4")
# except:
#     print "代码出错"
# nrows=sh.nrows #获取行数
# str=""
# for i in range(1,nrows):
#     row_data=sh.row_values(i,1)[0]
#     print row_data
#     str+=row_data+"\n"
#
# f=open("C:\\Users\\st\\Desktop\\HelloWorld\\sc.txt","w+")
# f.write(str)

import requests
from lxml import etree
import re
import time

#------------------------------提取页面urL----------------------------
# params={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"}
# response=requests.get("http://bbs.scol.com.cn/forum-41-1.html",params=None)
# response.encoding = 'gbk'
# text=response.text
# #xpath去匹配需要的数据
# selector=etree.HTML(text, parser=None, base_url=None)
# p_url="<a href=\"([\s\S]*?)\" onclick=\"atarget(this)\" class=\"s xst\">.*?</a>"
# title_url_list=re.findall(p_url,text)
#
# title_url_list=[]
# ulr1=selector.xpath('//th[@class="common"]//a[@class="s xst"]/@href')
# ulr2=selector.xpath('//th[@class="new"]//a[@class="s xst"]/@href')
# title_url_list=ulr1+ulr2


#提取信息------------------------------------------------------
# response=requests.get("http://bbs.scol.com.cn/thread-15172339-1-1.html?_dsign=f2f207c1")
# response.encoding = 'gb2312'
# text=response.text
# print text
#
# #xpath去匹配需要的数据
# selector=etree.HTML(text, parser=None, base_url=None)
# #标题
# title=selector.xpath('//h1[@class="ts"]//a[@id="thread_subject"]/text()')
# #发表日期
# date=selector.xpath('//em[@class="xg1"]/text()')
# # #发表内容,正则匹配
# content=selector.xpath('//td[@class="t_f"]//text()')
# #来源
# source=selector.xpath('//div[@id="pt"]//div[@class="z"]//a/text()')
# #发帖人
# author=selector.xpath('//div[@class="floor-profile"]//a/text()')
#
#
#
#
# data={}
# data["Ftitle"]=title[0].encode("utf-8") if title else ""
# Fdate=(date[0]+":00").encode("utf-8").replace("发表于 ","") if date else "Null"
# data["Fdate"]=time.strftime('%Y-%m-%d %H:%M:%S',time.strptime(Fdate,'%Y-%m-%d %H:%M:%S'))
# Fcontent=('').join(content).encode("utf-8") if content else ""
# data["Fcontent"]=Fcontent
# data["Flink"]="http://bbs.scol.com.cn/thread-15172568-1-1.html?_dsign=d3e54ac2"
# data["Ftype"]= "论坛" if re.search(u"论坛",source[2]) else "政务"
# data["Fsource"]= source[2] if source else ""
# data["FcreateTime"]=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
# data["Fauthor"]=author[0] if author else ""
# s="sd"
#
# print data["Ftitle"]
# print data["Fdate"]
# print data["Fcontent"]
# print data["Flink"]
# print data["Ftype"]
# print data["Fsource"]
# print data["FcreateTime"]
# print data["Fauthor"]

# s="上欧式机傻大个啥东关街我说的估计萨德公司的结果尚德机构是啊个"
# key_list=["上","大","我","是啊2"]
# def f(key):
#     if re.findall(key,s):
#         return True
#     else:
#         return False
# print map(f,key_list)

import random
n=random.randint(1,9999)
b=random.randint(1,9999)
print n+b











