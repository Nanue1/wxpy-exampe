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

    def __init__(self, wxbot):
        global bot
        bot = wxbot
        self.msg = bot.messages

    # 注册好友请求类消息
    # 自动接受验证信息中包含 '关键字' 的好友请求
    @bot.register(msg_types=FRIENDS)
    def auto_accept_friends(self, msg):
        # 判断好友请求中的验证文本
        if auto_accept_msg_keyword in msg.text.lower():
            # 接受好友 (msg.card 为该请求的用户对象)
            new_friend = msg.card.accept()
            # 添加时间备注
            new_friend.set_remark_name(Time.str_20171105() + new_friend.nick_name)
            # 向新的好友发送消息
            new_friend.send('哈哈，我自动接受了你的好友请求')

            # 打印来自其他好友、群聊和公众号的消息

    @bot.register()
    def print_others(self):
        return self.msg
    # 回复 my_friend 的消息 (优先匹配后注册的函数!)
    @bot.register()
    def reply_my_friend(self):
        return 'received: {} ({})'.format(self.msg.text, self.msg.type)
