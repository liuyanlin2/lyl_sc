#encoding=utf-8
import json
from django.shortcuts import render
import random
from dwebsocket.decorators import accept_websocket
import time
from multiplexing_class.base_view import date_handler
from multiplexing_class.mysql_helper import MysqlHelper


#主页
def Index(request):
    return render(request, 'index.html')
#爬虫管理页面
def SpiderMgr(request):
    return render(request, 'spider_mgr.html')
#任务派发管理
def TaskMgr(request):
    return render(request, 'task_mgr.html')
# 信息列表页面
def infoList(request):
    return render(request, 'info_list.html')
#关键词库
def keyWords(request):
    return render(request, 'key_words.html')

clients = []
@accept_websocket
def echo(request):
    if request.is_websocket:
        try:
            clients = []
            clients.append(request.websocket)
            for message in request.websocket:
                print len(clients)
                data=eval(message)
                while True:
                    if data["type"]==1:
                        sql_where=""
                        if data["ipSelect"]!="":
                            sql_where+="where FserverIp='{}'".format(data["ipSelect"])
                        result=MysqlHelper.excuteFindPages("tb_task","*",int(data["pageIndex"]),int(data["pageSize"]),sql_where,"order by Fid asc" )
                    elif data["type"]==2:
                        sql_where=""
                        table="(SELECT tb_spider.Fid,tb_spider.FspiderName,tb_spider.Ftype,tb_spider.Fwebsite,tb_spider.FtimeInterval," \
                                  "tb_spider.Fstate,tb_spider.FserverIp,COUNT(tb_data.Fid)as Fnum from tb_spider" \
                                  " LEFT JOIN tb_data ON tb_spider.FspiderName=tb_data.Fsource GROUP BY tb_spider.FspiderName) as tb_spider"
                        if data["ipSelect"]!="":
                            sql_where+="where FserverIp='{}'".format(data["ipSelect"])
                        result=MysqlHelper.excuteFindPages(table,"*",int(data["pageIndex"]),int(data["pageSize"]),sql_where,"order by Fid asc" )

                    for client in clients:
                        result_message=json.dumps(result,default=date_handler)
                        client.send(result_message)
                    time.sleep(1)
        except Exception as ex:
            print "异常----"
        finally:
            print "关闭"
            clients.remove(request.websocket)