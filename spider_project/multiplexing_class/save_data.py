#!/usr/bin/python
# -*- coding: utf-8 -*-
import sys
sys.path.append('/home/spider_project')
from elasticsearch import Elasticsearch
from spider_project.settings import ES_HOST,ES_PORT
from multiplexing_class.mysql_helper import MysqlHelper
import MySQLdb
from base_view import dictToSqlvalues
from multiplexing_class.utility_class import Utility


#保存数据类
class SaveData(object):

    """
        :param data_list: 要保存的数据列表
    """
    def __init__(self,spiderName,data_list):
        self.spiderName=spiderName
        self.data_list=data_list
    #批量保存数据
    def saveDataBatch(self):
        #获取ES搜索引擎数据库连接
        es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
        # #获取mysql连接
        try:
            for item in self.data_list:
                id=MysqlHelper.excuteInsertReturnId("tb_data",item)
                if id:
                    #向ES插入数据  index:索引，相当于mysql的数据库名,doc_type:相当于mysql的表名
                    istrue=es.create(index="scdel_index",id=int(id),doc_type="tb_data",body=item)["created"]
                    print "插入结果："
                    print istrue
        except Exception as ex:
            #出现异常将异常信息发送给管理员邮箱
            Utility().sendEmail('1279449172@qq.com','2215857915@qq.com','ggfcyiwvmtzgbaec',self.spiderName+' 爬虫异常',ex)
            raise ex



    #保存单条数据
    def saveData(self,item):
        #获取ES搜索引擎数据库连接
        es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
        #获取mysql连接
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            print "----数据保存中------"
            id=Utility().getId()
            #向ES插入数据  index:索引，相当于mysql的数据库名,doc_type:相当于mysql的表名
            istrue=es.create(index="scdel_index",id=id,doc_type="tb_data",body=item)["created"]
            if istrue:
                #向mysql中插入数据
                value_str=dictToSqlvalues(item)
                sql = "insert into tb_data set "+value_str
                count = cur.execute(sql)
                if count>0:
                    return True
                else:
                    return False
        except Exception as ex:
            print ex
            conn.rollback()
            #出现异常将异常信息发送给管理员邮箱
            Utility().sendEmail('1279449172@qq.com','2215857915@qq.com','ggfcyiwvmtzgbaec',self.spiderName+' 爬虫异常',ex)
            raise ex
        finally:
            cur.close()
            conn.commit()
            conn.close()


