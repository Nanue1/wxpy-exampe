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

# from messages import Messages

# 测试初始化机器人
from utils.times import Time

bot = Login().bot
# 初始化聊天机器人
tuling = Tuling(api_key='61eea024ed154d8f9d8a33e98547057a')

# 测试friends
# print Friends(bot).friends_count()
# for i in Friends(bot).all_friends_name():
# 中文输出
# print i
# print Friends(bot).sex_friends()
# print Friends(bot).search_friend(u'20171105-manue1')
# print Friends(bot).friends

# friends = Friends(bot).remark_name_search()
# print len(friends)
# Friends(bot).rename_users()
# 测试groups
groups_utils = Groups(bot)


# new_group = Groups(bot).create_group(friends,'20171104')
# print new_group


# 测试消息  顺序问题
@bot.register(except_self=False)
def tuling_reply(msg):
    tuling.do_reply(msg)


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
