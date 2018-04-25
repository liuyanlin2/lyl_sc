项目依赖包:
- python version==2.7
- pip install django==1.9.2 本项目使用的是django框架1.9.2版本
- pip install MsSQL-python 连接mysql数据库的支持包
- pip install redis 连接redis数据库的支持包
- pip install paramiko 创建linux远程主机的包
- pip install multiprocessing 多进程任务队列所需要的包
- apt-get install lxml
- pip install dwebsocket
- pip install selenium selenium是一个web应用程序测试工具（爬虫有时也会用）


--------------------------5.x版本的------------------------------------
elsearch
139.159.216.76主机的elsearch账户密码：3.1415926
因为es官方文档说es不能在roo账户下启动，所以新建了这个账户用于启动es

-----------------1.x版本的----------本项目用的这个---------------------
启动elasticsearch命令
进入到/home/elsearch/elasticsearch-1.7.3下执行nohup ./bin/elasticsearch
