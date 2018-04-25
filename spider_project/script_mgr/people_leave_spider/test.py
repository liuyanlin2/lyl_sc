# -*- coding: utf-8 -*-

# #------------------读数据---------------------------------
# fileName='C:\Users\st\Desktop\HelloWorld\weburl.xlsx'
# bk=xlrd.open_workbook(fileName)
# shxrange=range(bk.nsheets)
# try:
#     sh=bk.sheet_by_name("Sheet3")
# except:
#     print "代码出错"
# nrows=sh.nrows #获取行数
# str=""
# for i in range(1,nrows):
#     row_data=sh.row_values(i,1)[0]
#     print row_data
#     str+=row_data+"\n"
#
# f=open("C:\\Users\\st\\Desktop\\HelloWorld\\pe.txt","w+")
# f.write(str)
import requests
from lxml import etree
import re
import time
#------------------------------提取页面urL----------------------------
# params={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"}
# response=requests.get("http://liuyan.people.com.cn/list.php?fid=1888&display=1",params=params)
# response.encoding = 'gb2312'
# text=response.text
# #xpath去匹配需要的数据
# selector=etree.HTML(text, parser=None, base_url=None)
# title_url_list=selector.xpath('//h2//b//a/@href')
# print len(title_url_list)

#提取信息------------------------------------------------------
response=requests.get("http://liuyan.people.com.cn/thread.php?tid=4360240&display=1&page=1")
response.encoding = 'gb2312'
text=response.text

#xpath去匹配需要的数据
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
data["Flink"]="http://liuyan.people.com.cn/thread.php?tid=4360240&display=1&page=1"
data["Ftype"]="政务"
data["Fsource"]="人民网《地方领导留言板》"
data["FcreateTime"]=time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
data["Fauthor"]=date[0].replace(re.findall(r"\d{4}-\d+-\d+ \d{2}:\d+",date[0])[0],"") if date else ""

print data["Ftitle"]
print data["Fdate"]
print data["Fcontent"]
print data["Flink"]
print data["Ftype"]
print data["Fsource"]
print data["FcreateTime"]
print data["Fauthor"]