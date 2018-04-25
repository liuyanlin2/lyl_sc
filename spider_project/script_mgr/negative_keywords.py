# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')

class NegativeKeyWords:

    #获取负面关键词列表
    def getNegativeKeyWordsList(self):
        #读取文本文件里面的url
        file = open("../negative_keywords.txt")
        list=[]
        while True:
            line = file.readline()
            key=line.replace("\n","")
            if not line:
                file.close()
                break
            list+=key.split(" ")
        file.close()
        return list


