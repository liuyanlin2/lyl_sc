#encoding=utf-8
from multiplexing_class.mysql_helper import MysqlHelper
from elasticsearch import Elasticsearch
from spider_project.settings import ES_HOST,ES_PORT

#获取信息列表
def getInfoListBll(request):
    startTime=request.GET.get("startTime").encode("utf-8")
    endTime=request.GET.get("endTime").encode("utf-8")
    Ftype=request.GET.get("Ftype").encode("utf-8")
    pageIndex=int(request.GET.get("pageIndex"))
    pageSize=int(request.GET.get("pageSize"))
    searchText=request.GET.get("searchText").encode("utf-8")
    #获取ES搜索引擎数据库连接
    es = Elasticsearch([{'host':ES_HOST,'port':ES_PORT}])
    #数据查询语句
    query_where={
        "query":{
            "bool":{
                    "must":[],
                }
            },
            "from":(pageIndex-1)*pageSize,   #起始位置
            "size": pageSize, #每页条数
            "sort":{"Fdate":"desc"},
    }
    #查询总条数
    query_count={
        "query":{
            "bool":{
                    "must":[],
                }
            },
            "size":0
    }
    if startTime!="" and endTime!="":
        time={"range":{
                "Fdate":{
                    "gte":startTime,
                    "lte":endTime
                }
            }
        }
        query_where["query"]["bool"]["must"].append(time)
        query_count["query"]["bool"]["must"].append(time)
    if Ftype!="-1":
        type={ "match": { "Ftype": Ftype}}
        query_where["query"]["bool"]["must"].append(type)
        query_count["query"]["bool"]["must"].append(type)
    if searchText!="":
        content={
            "query_string":{
                    "default_field" : "Fcontent",
                    "query" :'"{}"'.format(request.GET.get("searchText"))
            }
        }
        query_where["query"]["bool"]["must"].append(content)
        query_count["query"]["bool"]["must"].append(content)
    data = es.search(index="scdel_index", body=query_where)["hits"]["hits"]
    count=es.search(index="scdel_index", body=query_count)["hits"]["total"]
    result={}
    result["pageSize"]=pageSize
    result["pageIndex"]=pageIndex
    result["totalCounts"]=count if count else 0
    result["pageSize"]=pageSize
    result["dataList"]=data if data else []
    result["totalPages"]=count/pageSize if count%pageSize<=0 else count/pageSize+1
    return result


























