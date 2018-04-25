# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')

class TianYaUrl:
    '''
        :param file_url:url文件地址
        :param pageNum:页数
        :param keywords_list :关键词列表
    '''
    def __init__(self,file_url,pageNum,keywords_list):
        self.file_url=file_url
        self.pageNum=pageNum
        self.keywords_list=keywords_list
    #获取所有模块的前pageNum页的url地址,循环拼接
    def getUrlAll(self):
        #读取文本文件里面的天涯论坛各个模块urL根据关键词拼接要爬取的页面
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
                for key in self.keywords_list:
                    list.append(url+"&nextid="+str(num)+"&k="+key["FkeyWord"])
                num+=1
        return list



    #http://bbs.tianya.cn/list.jsp?item=free&order=1&nextid=5&k=四川   天涯杂谈
    #http://bbs.tianya.cn/list.jsp?item=828&order=1&nextid=3&k=四川  百姓杂谈
    #http://bbs.tianya.cn/list.jsp?item=no110&grade=0&order=1&su=0&k=四川 网罗天下
    #http://bbs.tianya.cn/list.jsp?item=lookout&order=1&nextid=0&k=四川 了忘天涯
    #http://bbs.tianya.cn/list.jsp?item=63&order=1&nextid=1&k=四川 天涯社区四川