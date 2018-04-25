#! -*- coding: utf-8 -*-
import requests
import re
import time
import redis
from selenium import webdriver
'''
    print "------------------ip信息--------------------"
    print "ip地址：",item[0]
    print "端口号：",item[1]
'''
#快代理爬虫
def KuaiDaiLiSpider():
    urls=["http://www.kuaidaili.com/free/inha/","http://www.kuaidaili.com/free/intr/"]
    ip_list=[]
    for url in urls:
        response=requests.get(url)
        html=response.text
        pattern='<tr>\s+<td\sdata-title="IP">([\s\S]*?)</td>\s+<td\sdata-title="PORT">([\s\S]*?)</td>\s+'
        result=re.findall(pattern,html)
        for item in result:
            ip_item={}
            ip_item["ip"]=item[0]
            ip_item["port"]=item[1]
            ip_list.append(ip_item)
        time.sleep(2)
    return ip_list

#无忧代理IP
def GuoNeiGaoliSpider():
    driver=webdriver.PhantomJS("phantomjs-2.1.1-windows/bin/phantomjs.exe")
    driver.get("http://www.xicidaili.com/nn/")
    html=driver.page_source
    print html
    #pattern2='<tr\sclass="\S+">\s+<td\sclass="\S+"><img\ssrc="\S+"\salt="\S+"\s/></td>\s+<td>([\s\S]*?)</td>\s+<td>([\s\S]*?)</td>\s+<td>'
    if html:
        r= re.compile(r'<tr\sclass="\S+">\s+<td\sclass="\S+"><img\ssrc="\S+"\salt="\S+"\s/></td>\s+<td>([\s\S]*?)</td>\s+<td>([\s\S]*?)</td>\s+"/>')
        print r.findall(html)
    # ip_list=[]
    # for item in result:
    #     ip_item={}
    #     ip_item["ip"]=item[0]
    #     ip_item["port"]=item[1]
    # return ip_list




if __name__ == "__main__":
    conn=redis.Redis(host='117.174.84.243',port=6379) # host为主机的IP，port和db为默认值

    # istrue=conn.lpush("ip_list",[{"ip":"113.244.56.126","port":"80"}])
    # print istrue
    # print conn.llen("ip_list")
    GuoNeiGaoliSpider()

    # while True:
    #     ip_list=[]
    #     k_list=KuaiDaiLiSpider()
    #     ip_list+=k_list
    #     for ip in ip_list:
    #         istrue=conn.rpush("ip_list",ip)
    #         print istrue
    #     time.sleep(120)


