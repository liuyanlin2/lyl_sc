# encoding:utf-8
import redis
#redis连接帮助类
class RedisHelper:
    @staticmethod
    def getRedisConnect():
        conn=redis.Redis(host='127.0.0.1') # host为主机的IP，port和db为默认值
        return conn

    #像set集合插入数据
    @staticmethod
    def insertSetData(setName,data):
        #获取连接
        conn=RedisHelper.getRedisConnect()
        conn.spop(setName) #删除 set集合中上一次存入的数据
        istrue=conn.sadd(setName,data) #向set集合中存入新的数据
        return istrue
    #删除set集合
    @staticmethod
    def deleteSetData(setName):
        conn=RedisHelper.getRedisConnect()
        istrue=conn.spop(setName)
        return istrue
    @staticmethod
    def getSetResult(setName):
        conn=RedisHelper.getRedisConnect()
        data_list=conn.smembers(setName)
        num=0
        for x in data_list:
            num+=1
            if num==1:
                return x
            else:
                return []
    @staticmethod
    #url去去重,判断是否在url库中
    def urlFilter(url,list_name):
        conn=RedisHelper.getRedisConnect()
        list=conn.lrange(list_name,0,-1)
        if url in list:
            return True
        else:
            conn.rpush(list_name,url)
            return False
    #添加list插入数据
    @staticmethod
    def insertListData(list_name,data):
        conn=RedisHelper.getRedisConnect()
        istrue=conn.lpush(list_name,data)
        return istrue
    #追加数据
    @staticmethod
    def listAppendData(list_name,data):
        conn=RedisHelper.getRedisConnect()
        istrue=conn.rpush(list_name,data)
        return istrue

r=RedisHelper()
r.insertListData("mala_url","2")