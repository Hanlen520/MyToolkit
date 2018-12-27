#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/30 14:47
# @Author  : qingping.niu
# @File    : StartTime.py
# @desc    :

import os,time,datetime
import uiautomator2 as u2

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


def start(devices,appName):
    d = u2.connect(devices)
    # d(scrollable=True).scroll.to(text=u"Notes")
    d(scrollable=True).fling.horiz.forward()
    d(text=u"Notes").click()
    begin = datetime.datetime.now()
    # end = None
    if d(text="Notes").exists:
        end = datetime.datetime.now()
        k = (end - begin)
        print(k.total_seconds())
    print("dddd")





if __name__=="__main__":
    devices = getdevices()
    print(devices[0])
    start(devices[0],appName="Notes")