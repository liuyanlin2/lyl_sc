#encoding=utf-8
from multiplexing_class.mysql_helper import MysqlHelper
from multiplexing_class.Linux import Linux
import threading
import re

#修改
def upTaskBll(request):
    Fstate=request.GET.get("Fstate") #0 停止 1 启动
    Fid=request.GET.get("Fid")
    task=MysqlHelper.excuteFindOne("select * from tb_task where Fid={}".format(Fid))

    host = Linux("139.159.218.222", task["FuserName"], task["FpassWord"])
    host.connect()
    result={}
    if int(Fstate)==0:
        #-----------根据pid关闭端口进程-----------
        msg='netstat -apn | grep {}'.format(task["Fport"])
        port_result=host.send(msg)
        # isEnd=False
        for x in re.findall("(\d+)/python",port_result):
            res=host.send('kill -9 {}'.format(x.encode("utf-8")))
            if re.findall("root@scdel-02:.*?#",res):
                isEnd=True
            else:
                isEnd=False
        if isEnd:
            #修改任务爬虫状态
            upsql_task="update tb_task set Fstate=0 where Fid={}".format(Fid)
            upsal_spider="update tb_spider set Fstate=0 where FtaskId={}".format(Fid)
            MysqlHelper.excuteManySqlReturnBool([upsql_task,upsal_spider])
            result["istrue"]=True
            result["msg"]="停止成功！"
        else:
            result["istrue"]=False
            result["msg"]="停止失败！"
    elif int(Fstate)==1:
        msg='python '+task["FscriptAddress"]
        isStart=host.send(msg)
        p = re.compile('root@scdel-02:.*?#')
        if p.search(isStart):
            MysqlHelper.excuteUpdate("tb_task",{"Fstate":1},"Fid={}".format(Fid))
            result["istrue"]=True
            result["msg"]="启动成功！"
        else:
            result["istrue"]=False
            result["msg"]="启动失败！"
    host.close()
    return result
#设置
def setUpBll(request):
    mydata={}
    Fid=request.POST.get("Fid").encode("utf-8")
    mydata["FtaskName"]=request.POST.get("FtaskName").encode("utf-8")
    mydata["FserverIp"]=request.POST.get("FserverIp").encode("utf-8")
    mydata["FtimeInterval"]=request.POST.get("FtimeInterval").encode("utf-8")
    mydata["FscriptAddress"]=request.POST.get("FscriptAddress").encode("utf-8")
    mydata["FuserName"]=request.POST.get("FuserName").encode("utf-8")
    mydata["FpassWord"]=request.POST.get("FpassWord").encode("utf-8")
    mydata["Fport"]=request.POST.get("Fport").encode("utf-8")
    mydata["Fauthkey"]=request.POST.get("Fauthkey").encode("utf-8")
    istrue=MysqlHelper.excuteUpdate("tb_task",mydata,"Fid={}".format(Fid))
    result={}
    if istrue:
        result["istrue"]=True
        result["msg"]="设置成功！"
    else:
        result["istrue"]=False
        result["msg"]="设置失败！"
    return result
#获取单条信息
def getInfoByIdBll(request):
    Fid=request.GET.get("Fid")
    result=MysqlHelper.excuteFindOne("select * from tb_task where Fid={}".format(Fid))
    return result
