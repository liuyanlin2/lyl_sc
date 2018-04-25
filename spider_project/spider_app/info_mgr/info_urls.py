#encoding=utf-8
from django.conf.urls import url

from spider_app.info_mgr.info_views import getInfoList

urlpatterns = [

    url(r'^getInfoList/$', getInfoList, name="getInfoList"),#获取信息列表




]