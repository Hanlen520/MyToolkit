#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/11/14 18:02
# @Author  : qingping.niu
# @File    : filepath.py
# @desc    :

import sys,os
from os import path
import datetime,time

# begin = datetime.datetime.now()
# time.sleep(5)
# end = datetime.datetime.now()
# k = end - begin
# print(k.total_seconds())

# d = path.dirname(__file__)  #返回当前文件所在的目录
#
# a = os.path.realpath(__file__)
# c = os.path.dirname(os.path.realpath(__file__))
#
# print(d)
# print(a)
# print(c)
# print(os.getcwd())
#print(os.path.join(os.getcwd(),"test.txt"))


# parent_path = os.path.dirname(d) #获得d所在的目录,即d的父级目录
# parent_path  = os.path.dirname(parent_path) ##获得parent_path所在的目录即parent_path的父级目录
#
# abspath = path.abspath(d) #返回d所在目录规范的绝对路径

#cmd = "d:&&cd G:\gitworkspace\LauncherForPython\com\ftp"
#ss = os.popen(cmd)
#cmd = "adb install -r Singed_zipalign_JoyLauncher_google_v7.0.1.8.1114.1_201811141927_debug.apk"
#=os.popen(cmd)


rsDir = os.path.join(".","result")
if not os.path.exists(rsDir):
    os.makedirs(rsDir)


monkeyLog = os.path.join(rsDir,"monkeylog.txt")
print(monkeyLog)
