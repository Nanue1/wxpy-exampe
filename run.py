#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/11/4
import random
import time

from wxpy import *

from friends import Friends
from groups import Groups
from login import Login
from messages import Messages
from setting import *
from utils.times import Time

# 初始化聊天机器人
bot = Login().bot

tuling = Tuling(api_key=api_key)

friends_utils = Friends(bot)
groups_utils = Groups(bot)
messages_utils = Messages()


# 注意消息顺序问题
# 机器人自动回复好友消息
@bot.register(except_self=False)
def tuling_reply(msg):
    # 好友回复口令发送邀请
    if not invite_friend(msg):
        # 特定消息回复
        if not key_word_reply(msg):
            time.sleep(random.uniform(0.5, 1))
            if messages_utils.supported_msg_type(msg, reply_unsupported=True):
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
        for group in groups_utils.admin_groups():
            if msg.chat in group:
                break
            else:
                if msg.chat not in groups_utils.invite_counter:
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
        # 邀请入群
        groups_utils.invite_group(new_friend)

#  在群中回复被 @ 的消息
@bot.register(groups_utils.groups, TEXT)
def reply_other_group(msg):
    if msg.chat in groups_utils.groups and msg.is_at:
        if messages_utils.supported_msg_type(msg, reply_unsupported=True):
            tuling.do_reply(msg)

bot.join()
