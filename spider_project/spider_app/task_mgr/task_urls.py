#encoding=utf-8
from django.conf.urls import url

from spider_app.task_mgr.task_views import upTask,setUp,getInfoById

urlpatterns = [

    url(r'^upTask/$', upTask, name="upTask"),#修改
    url(r'^setUp/$', setUp, name="setUp"),#设置
    url(r'^getInfoById/$', getInfoById, name="getInfoById"),#获取单条信息





]