#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/4
from wxpy import *

from setting import *
from utils.times import Time


class Messages(object):
    '''
    1.处理好友请求
    '''

    def __init__(self):
        pass

    # 判断消息是否为支持回复的消息类型
    def supported_msg_type(self, msg):
        supported = (TEXT,)
        if msg.type in supported:
            return True

    # 验证入群口令
    def valid_code(self, msg):
        return group_code in msg.text.lower()
