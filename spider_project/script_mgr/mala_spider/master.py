# -*- coding: utf-8 -*-
from multiplexing_class.utility_class import Master
from script_mgr.mala_spider.mala_url import MaLaUrl
from script_mgr.mala_spider.spider import MaLaSpider



if __name__ == '__main__':
    url_list=MaLaUrl('mala_url.txt',3).getUrlAll()
    spider=MaLaSpider()
    master=Master(url_list,spider)
    master.start()