#! -*- coding: utf-8 -*-
import os, datetime
import shutil
import time
import re

def CpVideo():
    #目录路径
    base_dir = '/home/ljf/桌面/Agora_Recording_SDK_for_Linux_FULL/samples/20170808/dsad_080143'
    #文件列表
    list = os.listdir(base_dir)
    # print list

    #获取文件列表
    filelist = []
    for i in range(0, len(list)):
        #每个文件绝对路径
        path = os.path.join(base_dir, list[i])
        if os.path.isfile(path):
            filelist.append(list[i])
    for i in range(0, len(filelist)):
        path = os.path.join(base_dir, filelist[i])
        if os.path.isdir(path):
            continue
        timestamp = os.path.getmtime(path)
        # print timestamp
        ts1 = os.stat(path).st_mtime
        date = datetime.datetime.fromtimestamp(timestamp)
        fileName=list[i] #文件名称
        fileCreateTime=date.strftime('%Y-%m-%d') #创建时间
        # print fileName, ' 创建时间是: ', fileCreateTime
        # print fileName.split("_")[0]
        if re.findall(".mp4",fileName.split("_")[0]):
            print fileName, ' 创建时间是: ', fileCreateTime
            cp_path="/home/ljf/桌面/Agora_Recording_SDK_for_Linux_FULL/samples/20170808/dsad_080143"+fileName
            #将指定路径的文件复制到指定目录下
            shutil.copy(path, "/home/ljf/桌面/file")
            to_day=time.strftime('%Y-%m-%d')
            if fileCreateTime==to_day:
                os.remove("/home/ljf/桌面/Agora_Recording_SDK_for_Linux_FULL/samples/20170808/dsad_080143"+fileName)
                print True
            else:
                print False


if __name__ == '__main__':
    while True:
        CpVideo()
        time.sleep(60)


