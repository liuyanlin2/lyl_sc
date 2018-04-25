# -*- coding: utf-8 -*-
from xinlang_url import XinLangUrl



for x in range(10):
    try:
        print x
        if x==5:
            raise Exception("异常为"+str(x))
    except Exception as ex:
        print ex
        continue

