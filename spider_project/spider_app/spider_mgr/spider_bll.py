#encoding=utf-8
from multiplexing_class.mysql_helper import MysqlHelper
from multiplexing_class.Linux import Linux


#修改
def upSpiderBll(request):
    Fstate=request.GET.get("Fstate") #0 停止 1 启动
    Fid=request.GET.get("Fid")
    spider=MysqlHelper.excuteFindOne("select * from tb_spider where Fid={}".format(Fid))
    #连接远程主机
    host = Linux(spider["FserverIp"], spider["FuserName"], spider["FpassWord"])
    host.connect()
    result={}
    if int(Fstate)==0:
        istrue=MysqlHelper.excuteUpdate("tb_spider",{"Fstate":0},"Fid={}".format(Fid))
        isEnd=host.send('killall -9 python '+spider["FscriptAddress"])
        if istrue and isEnd:
            result["istrue"]=True
            result["msg"]="停止成功！"
        else:
            result["istrue"]=False
            result["msg"]="停止失败！"
    elif int(Fstate)==1:
        task=MysqlHelper.excuteFindOne("select * from tb_task where Fid={}".format(int(Fid)))
        if int(task["Fstate"])!=0:
            istrue=MysqlHelper.excuteUpdate("tb_spider",{"Fstate":1},"Fid={}".format(Fid))
            isStart=host.send('python '+spider["FscriptAddress"])
            host.close()
            if istrue and isStart:
                result["istrue"]=True
                result["msg"]="启动成功！"
            else:
                result["istrue"]=False
                result["msg"]="启动失败！"
        else:
            result["istrue"]=False
            result["msg"]="启动失败，请先去派发任务！"
    return result
#设置
def setUpBll(request):
    mydata={}
    Fid=request.POST.get("Fid").encode("utf-8")
    mydata["FspiderName"]=request.POST.get("FspiderName").encode("utf-8")
    mydata["FserverIp"]=request.POST.get("FserverIp").encode("utf-8")
    mydata["FtimeInterval"]=request.POST.get("FtimeInterval").encode("utf-8")
    mydata["FscriptAddress"]=request.POST.get("FscriptAddress").encode("utf-8").replace("\\","/")
    mydata["FuserName"]=request.POST.get("FuserName").encode("utf-8")
    mydata["FpassWord"]=request.POST.get("FpassWord").encode("utf-8")
    mydata["Fport"]=request.POST.get("Fport").encode("utf-8")
    mydata["Fauthkey"]=request.POST.get("Fauthkey").encode("utf-8")
    mydata["Fwebsite"]=request.POST.get("Fwebsite").encode("utf-8")
    mydata["Ftype"]=request.POST.get("Ftype").encode("utf-8")
    print mydata["FscriptAddress"]
    istrue=MysqlHelper.excuteUpdate("tb_spider",mydata,"Fid={}".format(Fid))
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
    result=MysqlHelper.excuteFindOne("select * from tb_spider where Fid={}".format(Fid))
    return result
