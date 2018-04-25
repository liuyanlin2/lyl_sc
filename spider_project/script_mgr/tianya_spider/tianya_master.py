#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')
from multiplexing_class.base_master import Master
from tianya_url import TianYaUrl
from tianya_spider import TianYaSpider
from multiplexing_class.mysql_helper import MysqlHelper

#麻辣社区爬取任务派发
if __name__ == "__main__":
    #代理ip
    proxies = { "http": "http://115.220.3.253:808", "https": "http://121.31.147.192:8123", }
    params={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"}
    spider=TianYaSpider(proxies,params,"","1002")
    file_url="tianya_url.txt"
    keywords_list=MysqlHelper.excuteFindAll("select FkeyWord from tb_keywords")
    page_url_list=TianYaUrl(file_url,3,keywords_list).getUrlAll()
    print len(page_url_list)
    master = Master(page_url_list,spider,"1002","tb_task")
    master.start()