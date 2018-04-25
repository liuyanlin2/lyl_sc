#encoding=utf-8
import json
from django.http import HttpResponse
from multiplexing_class.base_view import ResponseData, SUCCESS, date_handler, MyError, EXCEPTIONMSG
from spider_app.task_mgr.task_bll import upTaskBll,setUpBll,getInfoByIdBll


#修改
def upTask(request):
    responseData=ResponseData()
    try:
        result=upTaskBll(request)
        if result["istrue"]:
            responseData.msg=result["msg"]
            responseData.istrue=SUCCESS
        else:
            responseData.msg=result["msg"]
            responseData.istrue="false"
    except MyError,ex:
        responseData.msg=str(ex)
    except Exception,ex:
        responseData.msg=EXCEPTIONMSG
    return HttpResponse(json.dumps(responseData.__dict__),content_type="application/json")
#设置
def setUp(request):
    responseData=ResponseData()
    try:
        result=setUpBll(request)
        if result["istrue"]:
            responseData.msg=result["msg"]
            responseData.istrue=SUCCESS
        else:
            responseData.msg=result["msg"]
            responseData.istrue="false"
    except MyError,ex:
        responseData.msg=str(ex)
    except Exception,ex:
        responseData.msg=EXCEPTIONMSG
    return HttpResponse(json.dumps(responseData.__dict__),content_type="application/json")
#获取单条信息
def getInfoById(request):
    responseData=ResponseData()
    try:
        result=getInfoByIdBll(request)
        if result:
            responseData.result=result
            responseData.istrue=SUCCESS
    except MyError,ex:
        responseData.msg=str(ex)
    except Exception,ex:
        responseData.msg=EXCEPTIONMSG
    return HttpResponse(json.dumps(responseData.__dict__),content_type="application/json")