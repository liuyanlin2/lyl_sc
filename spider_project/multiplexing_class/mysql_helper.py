#!/usr/bin/python2.7
# encoding:utf-8
# import the logging library
import sys
sys.path.append('/home/spider_project')
import MySQLdb
import logging
from base_view import dictToSqlvalues
from spider_project.settings import MYSQL_PASSWD, MYSQL_DB,MYSQL_USERNAME,MYSQL_HOST
logger = logging.getLogger("db_error")
#from common_interface.time_helper import *
#mysql帮助类
class MysqlHelper:
    @staticmethod
    def getMyConnect():
        try:
            conn = MySQLdb.connect(host=MYSQL_HOST, user=MYSQL_USERNAME, passwd=MYSQL_PASSWD,port=3306,db=MYSQL_DB,charset="utf8")
            return conn
        except Exception as ex:
            logger.error("Mysql:mysql cann't connect!!!"
                        " message:%s"%(str(ex)))
            # MysqlHelper.getMyConnect()
    #单条插入语句
    @staticmethod
    def excuteInsert(tablename,data):
        """
        :param tablename: 表名
        :param data: 要插入的数据，为字典型{Fcode:'123123',Fname:'13212'}
        :return: True或False
        """
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            value_str=dictToSqlvalues(data)
            sql = "insert into "+tablename+" set "+value_str
            print sql
            count = cur.execute(sql)
            if count>0:
                return True
            else:
                return False
        except Exception as ex:
            logger.error("Mysql:tablename=(%s)\n"
                        "data=(%s)\n"
                        "message:%s"%(tablename,data,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.commit()
            conn.close()
    #单条插入语句
    @staticmethod
    def excuteInsertReturnId(tablename,data):
        """
        :param tablename: 表名
        :param data: 要插入的数据，为字典型{Fcode:'123123',Fname:'13212'}
        :return: 返回主键ID或'',类型为字符串
        """
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            value_str=dictToSqlvalues(data)
            sql = "insert into "+tablename+" set "+value_str
            print sql
            count = cur.execute(sql)
            if count>0:
                return str(int(conn.insert_id()))
            else:
                return ''
        except Exception as ex:
            logger.error("Mysql:tablename=(%s)\n"
                        "data=(%s)\n"
                        "message:%s"%(tablename,data,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.commit()
            conn.close()
    #sql="insert into tb_test(name1,name2.name3) values(%s,%s,%s)"
    #values = (('1','1','10'),('1','1','10'))
    @staticmethod
    def excuteInsertMany(sql,values):
        conn=MysqlHelper.getMyConnect(cursorclass = MySQLdb.cursors.DictCursor)
        cur=conn.cursor()
        try:
            count = cur.executemany(sql,values)
            conn.commit()
            return True
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "values=(%s)\n"
                        "message:%s"%(sql,values,str(ex)))
            print ex
            conn.rollback()
            raise ex
        finally:
            cur.close()
            conn.close()

    #修改操作
    @staticmethod
    def excuteUpdate(tabename,myvalues,mywhere):
        """
        :param tabename:表名
        :param myvalues:要修改的字段，类型为字典型{Fcode:'123123',Fname:'13212'}
        :param mywhere:要修改的条件
        :return:返回True或False
        """
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            value_str=dictToSqlvalues(myvalues)
            if mywhere!="":
                sql="update "+tabename+" set "+value_str+" where "+mywhere
            else:
                sql="update "+tabename+" set "+value_str
            count = cur.execute(sql)
            if count>0:
                return True
            else:
                return False
        except Exception as ex:
            logger.error("Mysql:tabename=(%s)\n"
                        "myvalues=(%s)\n"
                        "mywhere=(%s)\n"
                        "message:%s"%(tabename,myvalues,mywhere,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.commit()
            conn.close()

    #执行一个简单的增删改操作，返回true或false
    #"update tb_test set name='666' where id='2'
    #insert into tb_test(Fname11,Fpwd11) VALUES('1','2')
    @staticmethod
    def excuteSqlReturnBool(sql):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            print sql
            count = cur.execute(sql)

            if count>0:
                return True
            else:
                return False
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "message:%s"%(sql,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.commit()
            conn.close()

    #执行批量增删改sql语句事务操作，返回true或false
    @staticmethod
    def excuteManySqlReturnBool(sqls=[]):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            for index in sqls:
                if index:
                    count = cur.execute(index)
            conn.commit()
            return True
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "message:%s"%(sqls,str(ex)))
            print ex
            conn.rollback()
            raise ex
        finally:
            cur.close()
            conn.close()

    #"tb_test","id=1"
    @staticmethod
    def excuteDelete(tablename,mywhere):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            sql="delete from "+tablename+" where "+mywhere
            count = cur.execute(sql)
            if count>0:
                return True
            else:
                return False
        except Exception as ex:
            logger.error("Mysql:tablename=(%s)\n"
                        "mywhere=(%s)\n"
                        "message:%s"%(tablename,mywhere,str(ex)))
            raise ex
        finally:
            cur.close()
            conn.commit()
            conn.close()

    #执行一个查询语句，返回查询的第一行数据
    #"select * from tb_test"
    @staticmethod
    def excuteFindOne(sql):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        print sql
        try:
            count = cur.execute(sql)
            if count>0:
                result = cur.fetchone()
                return result #[x for x in result]
            else:
                return []
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "message:%s"%(sql,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.close()

    #执行一个查询语句，返回所有数据
    #"select * from tb_test"
    @staticmethod
    def excuteFindAll(sql):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            count = cur.execute(sql)
            if count>0:
                result = cur.fetchall()
                return [x for x in result]
            else:
                return []
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "message:%s"%(sql,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.close()

    #执行一个多个查询语句，返回字典结果
    #"select * from tb_test"
    @staticmethod
    def excuteFindMany(sql_dict):
        """
        :param sql_dict: 字典型，例：{"sql1":"select * from tb_test","sql2":"select * from tb_test"}
        :return: 返回字典型，例:{"sql1":[{},{},{}],"sql2":[{},{},{}]}
        """
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            result={}
            for key,value in sql_dict.items():
                count = cur.execute(value)
                if count>0:
                    data = cur.fetchall()
                    result[key]=[x for x in data]
                else:
                    result[key]=[]
            return result
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "message:%s"%(sql_dict,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.close()


    #执行一个存储过程，返回所有数据
    #"select * from tb_test"
    @staticmethod
    def excuteFindAllProc(proc_name,proc_args):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            cur.callproc(proc_name,proc_args)
            result =cur._rows
            return [x for x in result]
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "message:%s"%(proc_name,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.close()

    #执行一个查询语句，返回受影响的行数
    @staticmethod
    def excuteSqlReturnInt(sql):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            count = cur.execute(sql)
            return count
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "message:%s"%(sql,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.close()

    #执行一个sql语句，返回总行数
    @staticmethod
    def excuteSqlReturnCount(tablename,sqlwhere):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            sql="select COUNT(*) from "+tablename+" "+sqlwhere+""
            cur.execute(sql)
            totalCounts=int(cur._rows[0]["COUNT(*)"])
            return totalCounts
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "message:%s"%(sql,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.close()

    #检查是否存在
    @staticmethod
    def isExistReturnBool(tablename,sqlwhere):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            sql="select COUNT(*) from "+tablename+" "+sqlwhere+""
            cur.execute(sql)
            totalCounts=int(cur._rows[0]["COUNT(*)"])
            if totalCounts>0:
                return True
            return False
        except Exception as ex:
            logger.error("Mysql:sql=(%s)\n"
                        "message:%s"%(sql,str(ex)))
            print ex
            raise ex
        finally:
            cur.close()
            conn.close()

    #执行一个分页查询
    #"tb_test",1,2,"id","Fid>1"
    #select * from tb_test where Fid >=(select Fid from tb_test where Fid>1 Order By Fid limit 2,1) limit 2
    @staticmethod
    def excuteFindPages(tablename,fileds,pageIndex,pageSize,mywhere,myorder):
        """
        :param tablename: 表名,字符串，例 :'zj_user'
        :param pageIndex: 第多少页，字符串，例第二页:'2'
        :param pageSize: 每页显示多少条，字符串，例8条:'8'
        :param myorder: 排序字段order by createTime desc
        :param mywhere: 过滤条件，字符串，例:'FdptId='101' and Fstate='1''
        :return:
        """
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            sqlCount="select COUNT(*) from "+tablename+" "+mywhere+""
            sqlPage="select "+fileds+" from "+tablename+" "+mywhere+" "+myorder+" limit "+str((pageIndex-1)*pageSize)+","+str(pageSize)
            print sqlCount
            print sqlPage
            cur.execute(sqlCount)
            totalCounts=int(cur._rows[0]["COUNT(*)"])
            count = cur.execute(sqlPage)
            pagelistjson={
                "pageSize":pageSize,
                "pageIndex":pageIndex,
                "totalCounts":totalCounts,
                "totalPages":1,
                "dataList":[]
            }
            if count>0:
                result = cur.fetchall()
                if totalCounts%pageSize==0:
                    totalPages=totalCounts/pageSize
                else:
                    totalPages=totalCounts/pageSize+1
                pagelistjson["totalPages"]=totalPages
                pagelistjson["dataList"]=[x for x in result]
            return pagelistjson
        except Exception as ex:
            # logger.error("Mysql:分页错误"
            #             "message:%s"%(str(ex)))
            print ex
            raise ex
        finally:
            conn.commit()
            cur.close()
            conn.close()

    #批量插入
    @staticmethod
    def excuteInsertBatch(data_list,tablename):
        conn=MysqlHelper.getMyConnect()
        cur=conn.cursor(cursorclass = MySQLdb.cursors.DictCursor)
        try:
            for data in data_list:
                value_str=dictToSqlvalues(data)
                sql = "insert into "+tablename+" set "+value_str
                print sql
                count = cur.execute(sql)
                if count>0:
                    istrue=True
                    pass
                else:
                    istrue=False
            return istrue
        except Exception as ex:
            conn.rollback()
            print ex
            raise ex
        finally:
            cur.close()
            conn.commit()
            conn.close()

