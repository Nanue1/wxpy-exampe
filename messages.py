#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/4
from wxpy import *

from setting import *
from groups import Groups


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
        ignored = (SYSTEM,NOTE, FRIENDS)

        fallback_replies = {
            RECORDING: u'🙉',
            PICTURE: u'🙈',
            VIDEO: u'🙈',
        }
        if msg.type in supported:
            return True
        elif reply_unsupported and (msg.type not in ignored):
            msg.reply(fallback_replies.get(msg.type,u'🐒'))

    # 验证入群口令返回对应分类群组
    @staticmethod
    def valid_code_return_groups(msg):
        for group_code in group_codes.keys():
            if group_code in msg.text.lower():
                return group_codes[group_code]
        return False

    # 根据关键字回复
    @staticmethod
    def key_word_reply(msg):
        for reply, keywords in keyword_replies.items():
            for keyword in keywords:
                if keyword in msg.text.lower():
                    msg.reply(reply)
                    return True

    # 好友输入口令 发送邀请
    def invite_friend(self,msg,bot):
        if self.supported_msg_type(msg):
            return_groups_name = self.valid_code_return_groups(msg)
            if return_groups_name:
                Groups(bot).invite_group(msg.sender,return_groups_name)
                return True

