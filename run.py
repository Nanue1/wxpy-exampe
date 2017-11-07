#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/11/4
import random
import time

import subprocess
from functools import wraps
from pprint import pformat

import datetime

import os

import psutil as psutil
from wxpy import *
from wxpy.utils import start_new_thread

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
    if not messages_utils.invite_friend(msg,bot):
        # 特定消息回复
        if not messages_utils.key_word_reply(msg):
            time.sleep(random.uniform(0.5, 1))
            if messages_utils.supported_msg_type(msg, reply_unsupported=True):
                tuling.do_reply(msg)


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

'''
--------------------------远程执行命令-------------------------------------
'''

def _status_text():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(process.create_time())
    memory_usage = process.memory_info().rss

    if globals().get('bot'):
        messages = bot.messages
    else:
        messages = list()

    return '[now] {now:%H:%M:%S}\n[uptime] {uptime}\n[memory] {memory}\n[messages] {messages}'.format(
        now=datetime.datetime.now(),
        uptime=str(uptime).split('.')[0],
        memory='{:.2f} MB'.format(memory_usage / 1024 ** 2),
        messages=len(messages)
    )


def from_admin(msg):
    """
    判断 msg 的发送者是否为管理员
    """
    from_user = msg.member if isinstance(msg.chat, Group) else msg.sender
    return from_user in friends_utils.admin_friends()


def admin_auth(func):
    """
    装饰器: 验证函数的第 1 个参数 msg 是否来自 admins
    """
    @wraps(func)
    def wrapped(*args, **kwargs):
        msg = args[0]

        if from_admin(msg):
            return func(*args, **kwargs)
        else:
            raise ValueError('{} is not an admin!'.format(msg))
    return wrapped


def send_iter(receiver, iterable):
    """
    用迭代的方式发送多条消息
    :param receiver: 接收者
    :param iterable: 可迭代对象
    """

    if isinstance(iterable, str):
        raise TypeError

    for msg in iterable:
        receiver.send(msg)


def update_groups():
    yield 'updating groups...'
    for _group in groups_utils.admin_groups():
        _group.update()
        yield '{}: {}'.format(_group.name, len(_group))


process = psutil.Process()
def _status_text():
    uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(process.create_time())
    memory_usage = process.memory_info().rss

    if globals().get('bot'):
        messages = bot.messages
    else:
        messages = list()

    return '[now] {now:%H:%M:%S}\n[uptime] {uptime}\n[memory] {memory}\n[messages] {messages}'.format(
        now=datetime.datetime.now(),
        uptime=str(uptime).split('.')[0],
        memory='{:.2f} MB'.format(memory_usage / 1024 ** 2),
        messages=len(messages)
    )
def status_text():
    yield _status_text()
# 定时报告进程状态
def heartbeat():
    while bot.alive:
        time.sleep(600)
        # noinspection PyBroadException
        try:
            send_iter(groups_utils.admin_groups(), status_text())
        except:
            # logger
            pass
start_new_thread(heartbeat)


def _restart():
    os.execv(sys.executable, [sys.executable] + sys.argv)
def restart():
    yield 'restarting bot...'
    bot.core.dump()
    _restart()


def latency():
    yield '{:.2f}'.format(bot.messages[-1].latency)



# 远程命令 (单独发给机器人的消息)
remote_orders = {
    'g': update_groups,
    's': status_text,
    'r': restart,
    'l': latency,
}



def remote_shell(command):
    r = subprocess.run(
        command, shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        universal_newlines=True
    )
    if r.stdout:
        yield r.stdout
    else:
        yield '[OK]'

def remote_eval(source):
    try:
        ret = eval(source, globals())
    except (SyntaxError, NameError):
        raise ValueError('got SyntaxError or NameError in source')
    yield pformat(ret)

@admin_auth
def server_mgmt(msg):
    """
    服务器管理:
        若消息文本为为远程命令，则执行对应函数
        若消息文本以 ! 开头，则作为 shell 命令执行
        若不满足以上，则尝试直接将 msg.text 作为 Python 代码执行
    """
    order = remote_orders.get(msg.text.strip())
    if order:
        send_iter(msg.chat, order())
    elif msg.text.startswith('!'):
        command = msg.text[1:]
        send_iter(msg.chat, remote_shell(command))
    else:
        send_iter(msg.chat, remote_eval(msg.text))


@bot.register(groups_utils.admin_groups(), msg_types=TEXT, except_self=False)
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
        server_mgmt(msg)
    except ValueError:
        # 上述的 4.
        if isinstance(msg.chat, User):
            if messages_utils.supported_msg_type(msg, reply_unsupported=True):
                tuling.do_reply(msg)

bot.join()
