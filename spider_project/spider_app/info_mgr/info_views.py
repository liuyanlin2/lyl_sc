#encoding=utf-8
import json
from django.http import HttpResponse
from multiplexing_class.base_view import ResponseData, SUCCESS, date_handler, MyError, EXCEPTIONMSG
from spider_app.info_mgr.info_bll import getInfoListBll


#获取信息列表
def getInfoList(request):
    responseData=ResponseData()
    try:
        result=getInfoListBll(request)
        if result:
            responseData.result=result
            responseData.istrue=SUCCESS
        else:
            responseData.istrue="false"
    except MyError,ex:
        responseData.msg=str(ex)
    except Exception,ex:
        responseData.msg=EXCEPTIONMSG
    return HttpResponse(json.dumps(responseData.__dict__,default=date_handler),content_type="application/json")