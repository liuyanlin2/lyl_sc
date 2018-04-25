#!/usr/bin/python2.7
# encoding:utf-8
import sys
sys.path.append('/home/spider_project')
import hashlib
import json
import os
import uuid
import logging
import datetime
import redis
# from bson import ObjectId
from django.conf.global_settings import SECRET_KEY
from django.shortcuts import render
import StringIO
import xlwt
import time
from DjangoCaptcha import Captcha
from django.http import StreamingHttpResponse, HttpResponse, HttpResponseRedirect

logger = logging.getLogger("all_error")
api_log = logging.getLogger("api_error")
SUCCESS="success"
NODATA="nodata"
ERROR="error"
NOLOGIN="nologin"
COOKIE_TIME=259200
EXCEPTIONMSG="操作异常，请与管理员联系活稍后重试"
class ResponseData:
    def __init__(self):
        self.istrue=ERROR
        self.msg="操作失败"
        self.result=None


#自定义异常，用于验证
class MyError(Exception):
    pass

#判断验证码是否正确
def validateCode(request):
    _code = request.POST.get('code') or ''
    ca = Captcha(request)
    if ca.check(_code):
        return True
    else:
        return False

#时间格式转换
def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return str(obj)
    elif isinstance(obj,datetime.timedelta):
        return str(obj)
    # elif isinstance(obj, ObjectId):
    #     return str(obj)
    else:
        raise TypeError

#获取文件的扩展品（后缀名）
def file_extension(path):
  return os.path.splitext(path)[1]

#MD5加密
def md5Password(str):
    m = hashlib.md5(SECRET_KEY)
    m.update(str)
    return "mm+"+m.hexdigest()
#转换为字典里面的数据全部转化为str
def dictToStr(data):
    result={}
    for x,y in data.items():
        if isinstance(x,unicode):
            x=x.encode("utf-8")
        if isinstance(y,unicode):
            y=y.encode("utf-8")
        result[str(x)]=str(y)
    return result
#转换为字典里面的数据全部转化为例Fcode='123123',Fname='31321'字符串
def dictToSqlvalues(data):
    try:
        result=dictToStr(data)
        result_list=[]
        for x,y in result.items():
            if y=="Null":
                value=x+"="+y
            else:
                value=x+"='"+y+"'"
            result_list.append(value)
        return ",".join(result_list)
    except TypeError,e:
        raise e

#把字典的values转换为格式（'idif','jsd123','124123'）字符串
def dictValuesToStr(data):
    try:
        result=dictToStr(data)
        return "("+",".join(["'"+x+"'" for x in result.itervalues()])+")"
    except TypeError,e:
        raise e

#把列表的值拼接成'sdf','sdfsd','sdfsdf'的字符串
def listToStr(data):
    try:
        result=[]
        for x in data:
            if isinstance(x,unicode):
                x=x.encode("utf-8")
            result.append("'"+str(x)+"'")
        return ",".join(result)
    except TypeError,e:
        raise e

#获取唯一ID
def getSoleId():
    _result=str(uuid.uuid4())
    return _result

#分页拼接公用方法
def pageSplice(page_list,side_table,splice_key):
    """
    :param page_list: 分页查询出来的列表，
    :param side_table: 要拼接的列表，json数组，例[{},{}]
    :param splice_key: 拼接数组的命名
    :return: 返回分页列表
    """
    for index,primary in enumerate(page_list["dataList"]):
        data=[]
        for side in side_table:
            if str(primary["Fid"])==str(side["FuserId"]):
                data.append(side)
        page_list["dataList"][index][splice_key]=data
    return page_list



#判断是否是合法的日期
def isVaildDate(date):
    try:
        if ":" in date:
            time.strptime(date, "%Y-%m-%d %H:%M:%S")
        else:
            time.strptime(date, "%Y-%m-%d")
        return True
    except:
        return False
#判断是否是数字
def isInt(data):
    if data.isdigit():
        return True
    else:
        return False
#批量插入时用的值的帮助类
class insertValues:
    def __init__(self):
        self.data=[]
    #追加内容例['iserwe','wewerwer']
    def append(self,x):
        if isinstance(x,unicode):
            x=x.encode("utf-8")
        self.data.append("'"+x+"'")
    #列表转字符串例('werwer','sdgsdf')
    def toString(self):
        return "("+",".join(self.data)+")"

#取值封装
def getPostGet(request,key,default=""):
    key_str=request.POST.get(key,"").strip() if request.method == "POST" else request.GET.get(key,"").strip()
    if isinstance(key_str,unicode):
        key_str=key_str.encode("utf-8")
    if key_str=="":
        key_str=default
    return key_str


