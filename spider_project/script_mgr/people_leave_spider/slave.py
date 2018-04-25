# -*- coding: utf-8 -*-

from multiplexing_class.utility_class import Slave
from script_mgr.people_leave_spider.spider import PeopleSpider

if __name__ == '__main__':
    proxies_list = [
        {"http": "http://115.220.3.253:808"},
        {"http": "http://115.320.3.253:808"},
        {"http": "http://834.220.3.253:808"}
    ]

    params_list = [
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"},
        {
            "User-Agent": "Mozilla/5.0 (Windows NT 7.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"},
        {
            "User-Agent": "Mozilla/5.0 (Windows NT xp.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"}
    ]
    spider = PeopleSpider(proxies_list=proxies_list, params_list=params_list)
    slave=Slave(spider)
    slave.start()