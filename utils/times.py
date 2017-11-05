#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/5
import time

class Time(object):
    def __init__(self):
        self.now = time.localtime(time.time())

    # r str 20171105
    def str_20171105(self):
        return time.strftime("%Y%m%d", self.now)
