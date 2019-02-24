#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/15 18:52
# @Author  : qingping.niu
# @File    : runingMeminfo.py
# @desc    : APK运行时RAM的占用情况
"""
每隔1分钟记录一次meminfo数据
"""
import os,subprocess,time

rsDir = os.path.join(".","result")
print(rsDir)
if not os.path.exists(rsDir):
    os.makedirs(rsDir)

print("日志路径:"+rsDir)

monkeyLog = os.path.join(rsDir,"monkeylog.txt")
logcatLog = os.path.join(rsDir,"logcat.txt")
rsFilePath = os.path.join(rsDir,"result.txt")

def getPid(devices):
    output = subprocess.getoutput("adb -s %s shell ps |findstr monkey"%devices)
    if len(output)>0 and "error" not in output and output !='':
        print("True")
        return True
    else:
        print("False")
        return False

def runMonkey(packagename,devices):
    event = "adb -s %s shell monkey -p %s -s 10 --pct-touch 30 --throttle 300 -v 10000 --monitor-native-crashes > %s" %(devices,packagename,monkeyLog)
    subprocess.Popen(event,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
    time.sleep(2)
    count =1
    while getPid(devices):
        meminfoPath = os.path.join(rsDir,"meminfo%s.txt"%count)
        cmd = "adb -s %s shell dumpsys -t 50 meminfo --oom> %s"%(devices,meminfoPath)
        subprocess.Popen(cmd,shell=True,stderr=subprocess.PIPE,stdout=subprocess.PIPE)
        time.sleep(2*60)
        count += 1
    readFile(packagename,count)

def readFile(packagename,count):
    rs = []
    for i in range(1,count):
        temp=[]
        fileName = "meminfo%s.txt"%i
        file = open(os.path.join(rsDir,fileName),"r")
        rs.append(fileName)
        lines = file.readlines()
        for line in lines:
            # print(line)
            # if "Total PSS by OOM adjustment" in line:
            #     break;
            # else:
            if packagename in line:
                temp.append(line)
        rs.append(temp)

    rsFile = open(rsFilePath, "w")
    for line in rs:
        rsFile.write(str(line)+"\n")
    rsFile.close()

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

#可选
def logcat(devices):
    cmd = 'adb -s %s logcat -c && adb logcat -v time *:E > %s'%(devices,logcatLog)
    subprocess.Popen(cmd,shell=True)


if __name__=="__main__":
    dict = {
        "1":"com.tct.note",
        "2":"com.tct.calculator",
        "3":"com.tct.video",
        "4":"com.hawk.android.browser",
        "5":"com.tct.calendar",
        "6":"com.gameloft.android.GloftSOMP"
    }
    print("""
        获取RAM运行时内存,间隔2分钟一次
        1.com.tct.note
        2.com.tct.calculator
        3.com.tct.video
        4.com.hawk.android.browser
        5.com.tct.calendar
        6.com.gameloft.android.GloftSOMP
    """)
    val = input("请输入对应包名序号:")
    packageName = dict[val]
    devices = getdevices()
    if len(devices)>0:
        runMonkey(packagename=packageName,devices=devices[0])
    else:
        print("设备连接异常")


