#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/11/4
import time
import traceback

from wxpy import *
from setting import *
from login import Login

from friends import Friends
from groups import Groups

from messages import Messages
# from messages import Messages

# 测试初始化机器人
from utils.times import Time

bot = Login().bot
# 初始化聊天机器人
tuling = Tuling(api_key='61eea024ed154d8f9d8a33e98547057a')

friends_utils = Friends(bot)
groups_utils = Groups(bot)
messages_utils = Messages()


# new_group = Groups(bot).create_group(friends,'20171104')
# print new_group


# 注意消息顺序问题
# 机器人自动回复好友消息
@bot.register(friends_utils.friends, except_self=False)
def tuling_reply(msg):
    # 好友回复口令发送邀请
    if not invite_friend(msg):
        # 特点消息回复
        if not key_word_reply(msg):
            tuling.do_reply(msg)


# 根据关键字回复
def key_word_reply(msg):
    for reply, keywords in keyword_replies.items():
        for keyword in keywords:
            if keyword in msg.text.lower():
                msg.reply(reply)
                return True


# 好友输入口令 发送邀请
def invite_friend(msg):
    if messages_utils.supported_msg_type(msg):
        if messages_utils.valid_code(msg):
            groups_utils.invite_group(msg.sender)
            return True


# 手动添加好友后提示信息
@bot.register(msg_types=NOTE)
def manually_added(msg):
    if u'现在可以开始聊天了' in msg.text:
        # 延迟发送更容易引起注意
        time.sleep(2)
        return u'你好呀，{}，还记得咱们的入群口令吗？回复口令即可获取入群邀请。'.format(msg.chat.name)


# 注册好友请求类消息
# 自动接受验证信息中包含 '关键字' 的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本
    if auto_accept_msg_keyword in msg.text.lower():
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = msg.card.accept()
        # 添加时间备注
        new_friend.set_remark_name(Time().str_20171105() + '-' + new_friend.nick_name)
        # 向新的好友发送消息
        # new_friend.send(new_friend_text)
        # 邀请入群
        groups_utils.invite_group(new_friend)


bot.join()
