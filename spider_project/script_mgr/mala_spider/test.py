# -*- coding: utf-8 -*-
import random

# proxies_list = [{ "http": "http://115.220.3.253:808"},{ "http": "http://115.320.3.253:808"},{ "http": "http://834.220.3.253:808"}]
# params_list=[{"User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"},
#              {"User-Agent":"Mozilla/5.0 (Windows NT 7.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"},
#              {"User-Agent":"Mozilla/5.0 (Windows NT xp.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3000.4 Safari/537.36"}
#              ]
#
#
# s=random.choice (proxies_list)
# print s



# from time import strftime,gmtime
#
# print strftime("%Y-%m-%d", gmtime())
#
#
# if str(strftime("%Y-%m-%d", gmtime()))=='2017-07-23':
#     print True
# else:
#     print False
from lxml import etree