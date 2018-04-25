# -*- coding: utf-8 -*-
from multiplexing_class.utility_class import Master
from script_mgr.people_leave_spider.people_leave_url import PeopleUrl
from script_mgr.people_leave_spider.spider import PeopleSpider



if __name__ == '__main__':
    url_list=PeopleUrl('people_leave_url.txt',3).getUrlAll()
    spider=PeopleSpider()
    master=Master(url_list,spider)
    master.start()