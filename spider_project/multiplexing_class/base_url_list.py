# -*- coding: utf-8 -*-
#url类，用于获取要爬取的信息链接地址
class UrlList:

    '''
        :param file_url:url文件地址
        :param pageNum:页数
    '''
    def __init__(self,file_url,pageNum):
        self.file_url=file_url
        self.pageNum=pageNum
    #获取所有地方论坛的前2页url地址,循环拼接
    def getUrlAll(self):
        #读取文本文件里面的各个地方论坛首页地址
        file = open(self.file_url)
        list=[]
        while True:
            line = file.readline()
            url=line.replace("\n","")
            if not line:
                file.close()
                break
            num=0
            for x in range(self.pageNum):
                num+=1
                list.append(url[0:-6]+str(num)+".html")
        return list