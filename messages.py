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
    @staticmethod
    def supported_msg_type(msg, reply_unsupported=False):
        supported = (TEXT,)
        ignored = (SYSTEM,NOTE , FRIENDS)

        fallback_replies = {
            RECORDING : u'🙉',
            PICTURE: u'🙈',
            VIDEO: u'🙈',
        }
        if msg.type in supported:
            return True
        elif reply_unsupported and (msg.type not in ignored):
            msg.reply(fallback_replies.get(msg.type,u'🐒'))

    # 验证入群口令
    @staticmethod
    def valid_code(msg):
        return group_code in msg.text.lower()

