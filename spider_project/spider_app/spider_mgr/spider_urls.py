#encoding=utf-8
from django.conf.urls import url

from spider_app.spider_mgr.spider_views import upSpider,setUp,getInfoById

urlpatterns = [

    url(r'^upSpider/$', upSpider, name="upSpider"),#修改
    url(r'^setUp/$', setUp, name="setUp"),#设置
    url(r'^getInfoById/$', getInfoById, name="getInfoById"),#获取单条信息




]