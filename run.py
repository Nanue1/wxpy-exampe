#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/11/4
import random
import time

from wxpy import *
from wxpy.utils import start_new_thread

from friends import Friends
from groups import Groups
from commands import Commands
from login import Login
from messages import Messages
from setting import *
from utils.times import Time
from logger import Logger

# 初始化聊天机器人
bot = Login().bot
# 初始化图灵机器人
tuling = Tuling(api_key=api_key)

logger = Logger(bot).init_logger()
friends_utils = Friends(bot)
groups_utils = Groups(bot)
messages_utils = Messages()
commands_utils = Commands(bot)


# 机器人自动回复好友消息
@bot.register(except_self=True)
def tuling_reply(msg):
    # 好友回复口令发送邀请
    if not messages_utils.invite_friend(msg, bot):
        # 只自动回复好友消息
        if isinstance(msg.chat, User):
            if messages_utils.supported_msg_type(msg, reply_unsupported=True):
                # 特定消息回复
                if not messages_utils.key_word_reply(msg):
                    time.sleep(random.uniform(0.2, 1))
                    tuling.do_reply(msg)


# 手动添加好友后提示信息
@bot.register(msg_types=NOTE, except_self=True)
def manually_added(msg):
    if u'现在可以开始聊天了' in msg.text:
        # 延迟发送更容易引起注意
        time.sleep(2)
        for group in groups_utils.user_groups():
            if msg.chat in group:
                break
            else:
                if msg.chat not in groups_utils.invite_counter:
                    return u'你好呀，{}，还记得咱们的入群口令吗？回复口令即可获取入群邀请。'.format(msg.chat.name)


# 自动接受验证信息中包含 '关键字' 的好友请求
@bot.register(msg_types=FRIENDS)
def auto_accept_friends(msg):
    # 判断好友请求中的验证文本,如果正确返回群组
    return_groups = messages_utils.valid_code_return_groups(msg)
    if return_groups:
        # 接受好友 (msg.card 为该请求的用户对象)
        new_friend = msg.card.accept()
        # 添加时间备注
        new_friend.set_remark_name(Time().str_20171105() + '-' + new_friend.nick_name)
        # 邀请入群
        groups_utils.invite_group(new_friend,return_groups)


# 在群中回复被 @ 的消息
@bot.register(groups_utils.groups, TEXT)
def reply_group(msg):
    if msg.chat in groups_utils.groups and msg.is_at:
        if messages_utils.supported_msg_type(msg, reply_unsupported=True):
            tuling.do_reply(msg)


# 远程管理组执行命令
@bot.register(groups_utils.admin_group(), msg_types=TEXT)
def reply_admins(msg):
    """
    响应远程管理员
    内容解析方式优先级：
    1. 若为远程命令，则执行远程命令 (额外定义，一条命令对应一个函数)
    2. 若消息文本以 ! 开头，则作为 shell 命令执行
    3. 尝试作为 Python 代码执行 (可执行大部分 Python 代码)
    4. 若以上不满足或尝试失败，则作为普通聊天内容回复
    """
    try:
        # 上述的 1. 2. 3.
        commands_utils.server_mgmt(msg)
    except ValueError:
        # 上述的 4.
        if isinstance(msg.chat, User):
            if messages_utils.supported_msg_type(msg, reply_unsupported=True):
                tuling.do_reply(msg)


start_new_thread(commands_utils.heartbeat)

bot.join()
