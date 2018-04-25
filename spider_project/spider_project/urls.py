#encoding=utf-8
from django.conf.urls import url,include
from django.contrib import admin
from spider_project.views import Index,SpiderMgr,TaskMgr,echo,infoList,keyWords

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$',Index, name="index"), #主页
    url(r'^spider_mgr/', SpiderMgr, name="spider_mgr"),#爬虫管理页面
    url(r'^task_mgr/', TaskMgr, name="task_mgr"),#任务派发管理
    url(r'^echo$', echo,name='echo'),#连接websocket
    url(r'^info_list/', infoList,name='info_list'),#信息列表
    url(r'^key_words/', keyWords,name='key_words'),#关键词库

    url(r'^spider_app/spider_mgr/', include('spider_app.spider_mgr.spider_urls')),#爬虫后台管理模块
    url(r'^spider_app/task_mgr/', include('spider_app.task_mgr.task_urls')),#任务派发后台管理
    url(r'^spider_app/info_mgr/', include('spider_app.info_mgr.info_urls')),#信息查询后台管理
]
