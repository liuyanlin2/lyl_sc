# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')

class XinLangUrl:
    '''
        :param file_url:url文件地址
        :param pageNum:页数
    '''
    def __init__(self,file_url,pageNum):
        self.file_url=file_url
        self.pageNum=pageNum
    #获取所有模块的前pageNum页的url地址,循环拼接
    def getUrlAll(self):
        #读取文本文件里面的url
        file = open(self.file_url)
        list=[]
        # while True:
        line = file.readline()
        url=line.replace("\n","")
        for x in range(self.pageNum):
            new_url=url+str(x+1)+".html"
            list.append(new_url)
        file.close()
        return list
