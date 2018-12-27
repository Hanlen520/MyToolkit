#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/23 10:54
# @Author  : qingping.niu
# @File    : Rom.py
# @desc    :

import os,subprocess


APP_ARCHITECTURE_TYPE_32 = 32
APP_ARCHITECTURE_TYPE_64 = 64

rsDir = os.path.join(".","result")
if not os.path.exists(rsDir):
    os.makedirs(rsDir)

print("日志路径:"+rsDir)

romResultPath = os.path.join(rsDir,"rom.txt")


def getapp_architechture_type(packagename):
    '''获取32or64位的APP'''
    output_64 = subprocess.getoutput('adb shell ps | findstr zygote64')
    if len(output_64)>0:
        # 64位中一定包含32位,先查应用是否属性64位
        pid_64 = output_64.split()[1]
        appList = os.popen('adb shell ps | findstr %s' % pid_64).readlines()
        ramis64=False
        if appList is not None:
            for line in appList:
                if packagename in line:
                    ramis64 = True
            if ramis64 is True:
                return APP_ARCHITECTURE_TYPE_64
            else:
                return APP_ARCHITECTURE_TYPE_32

    else:
        return APP_ARCHITECTURE_TYPE_32



def get_appromsize(packagename,devices):
    apksize = []
    loglist = []
    #获取应用路径
    cmd='adb -s %s shell pm path %s'%(devices,packagename)
    # output = os.popen(cmd).readline()
    output = subprocess.getoutput(cmd)
    path = output.split(':')[1]
    #获取base大小
    cmd1 = 'adb -s %s shell du -h %s'%(devices,path)

    output1 = os.popen(cmd1).readline()
    baseapk_size = output1.split()[0]
    apksize.append(baseapk_size)

    apkpath = path[0:path.rfind('/')]
    apkname = path[path.rfind('/')+1:path.rfind('.')]

    loglist.append(path)
    loglist.append(output1)

    arm_odex_path = 'adb -s %s shell du -h %s%s%s%s'%(devices,apkpath,'/oat/arm/',apkname,'.odex')
    arm_vdex_path = 'adb -s %s shell du -h %s%s%s%s'%(devices,apkpath,'/oat/arm/',apkname,'.vdex')
    arm64_odex_apth ='adb -s %s shell du -h %s%s%s%s'%(devices,apkpath,'/oat/arm64/',apkname,'.odex')
    arm64_vdex_path ='adb -s %s shell du -h %s%s%s%s'%(devices,apkpath,'/oat/arm64/',apkname,'.vdex')

    try:
        # cpu_type = getcpu_architecture_type()
        app_type = getapp_architechture_type(packagename)

        if app_type == 32:
            arm_odex_rs = os.popen(arm_odex_path).read()
            arm_odex_size = arm_odex_rs.split()[0]
            apksize.append(arm_odex_size)
            loglist.append(arm_odex_rs)

            arm_vdex_rs = os.popen(arm_vdex_path).read()
            if 'du:' not in arm_vdex_rs and len(arm_vdex_rs) >0:
                arm_vdex_size = arm_vdex_rs.split()[0]
                apksize.append(arm_vdex_size)
                loglist.append(arm_vdex_rs)
        else:
            arm64_odex_rs = os.popen(arm64_odex_apth).read()
            arm64_odex_size = arm64_odex_rs.split()[0]
            apksize.append(arm64_odex_size)
            loglist.append(arm64_odex_rs)
            arm64_vdex_rs = os.popen(arm64_vdex_path).read()

            if 'du:' not in arm64_vdex_rs and len(arm64_vdex_rs) >0:
                arm64_vdex_size = arm64_vdex_rs.split()[0]
                print(arm64_vdex_size)
                apksize.append(arm64_vdex_size)
                loglist.append(arm64_vdex_rs)
    except Exception as e:
        print(e)

    file = open(romResultPath, "w")
    for line in loglist:
        print(line)
        file.write(line+"\n")
    file.close()

def getdevices():
    devices = []
    result = os.popen("adb devices").readlines()
    result.reverse()
    try:
        for line in result:
            li = line.strip()
            if not len(li) or "attached" in li or "?" in li or "offline" in li:
                continue
            else:
                devices.append(li.split()[0])
        return devices
    except Exception as e:
        print(e)



if __name__=="__main__":
    dict = {
        "1":"com.tct.note",
        "2":"com.tct.calculator",
        "3":"com.tct.video",
        "4":"com.hawk.android.browser",
        "5":"com.tct.calendar",
        "6":"com.gameloft.android.GloftMC4M"
    }
    print("""
        获取RAM运行时内存,间隔1分钟一次
        1.com.tct.note
        2.com.tct.calculator
        3.com.tct.video
        4.com.hawk.android.browser
        5.com.tct.calendar
        6.com.gameloft.android.GloftMC4M
    """)
    val = input("请输入对应包名序号:")
    packageName = dict[val]
    devices = getdevices()
    if len(devices)>0:
        get_appromsize(packagename=packageName,devices=devices[0])
    else:
        print("设备连接异常")
