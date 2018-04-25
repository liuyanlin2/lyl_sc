#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')
from multiplexing_class.base_master import Master
from xinlang_url import XinLangUrl
from xinlang_spider import XinLangSpider
from multiplexing_class.mysql_helper import MysqlHelper

#新浪爬取任务派发
if __name__ == "__main__":
    #代理ip
    proxies = { "http": "http://115.220.3.253:808", "https": "http://121.31.147.192:8123", }
    params={"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"}
    spider=XinLangSpider(proxies,params,"","1003")
    file_url="xinlang_url.txt"
    page_url_list=XinLangUrl(file_url,20).getUrlAll()
    master = Master(page_url_list,spider,"1003","tb_task")
    master.start()