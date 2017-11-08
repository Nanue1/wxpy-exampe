#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/11/4
import datetime
import os
import subprocess
import sys
from pprint import pformat

import psutil
from wxpy import Group

from friends import Friends
from groups import Groups


class Commands(object):
    '''
    1. 远程重启
    '''

    def __init__(self, bot):
        self.bot = bot
        self.process = psutil.Process()
        self.friends_utils = Friends(bot)
        self.groups_utils = Groups(bot)
        # 远程命令 (单独发给机器人的消息)
        self.remote_orders = {
            'g': self._update_groups,
            's': self._status_text,
            'r': self._restart,
            'l': self._latency,
        }

    def _from_admins(self, msg):
        """
        判断 msg 的发送者是否为管理员
        """
        from_user = msg.member if isinstance(msg.chat, Group) else msg.sender
        return from_user in self.friends_utils.admin_friends()

    # def _admin_auth(self, func):
    #     """
    #     装饰器: 验证函数的第 1 个参数 msg 是否来自 admins
    #     """
    #     @wraps(func)
    #     def wrapped(*args, **kwargs):
    #         msg = args[0]
    #         if self._from_admin(msg):
    #             return func(*args, **kwargs)
    #         else:
    #             raise ValueError('{} is not an admin!'.format(msg))
    #     return wrapped
    @staticmethod
    def _send_iter(receiver, iterable):
        """
        用迭代的方式发送多条消息
        :param receiver: 接收者
        :param iterable: 可迭代对象
        """
        if isinstance(iterable, str):
            raise TypeError

        for msg in iterable:
            receiver.send(msg)

    @staticmethod
    def _remote_shell(command):
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

    @staticmethod
    def _remote_eval(source):
        try:
            ret = eval(source, globals())
        except (SyntaxError, NameError):
            raise ValueError('got SyntaxError or NameError in source')
        yield pformat(ret)

    def _update_groups(self):
        yield 'updating groups...'
        for _group in self.groups_utils.user_groups():
            _group.update()
            yield '{}: {}'.format(_group.name, len(_group))

    def _restart(self):
        yield 'restarting bot...'
        self.bot.core.dump()
        os.execv(sys.executable, [sys.executable] + sys.argv)

    def _latency(self):
        yield '{:.2f}'.format(self.bot.messages[-1].latency)

    def _status_text(self):
        uptime = datetime.datetime.now() - datetime.datetime.fromtimestamp(self.process.create_time())
        memory_usage = self.process.memory_info().rss

        if globals().get('bot'):
            messages = self.bot.messages
        else:
            messages = list()
        yield '[now] {now:%H:%M:%S}\n[uptime] {uptime}\n[memory] {memory}\n[messages] {messages}'.format(
            now=datetime.datetime.now(),
            uptime=str(uptime).split('.')[0],
            memory='{:.2f} MB'.format(memory_usage / 1024 ** 2),
            messages=len(messages)
        )

    # 定时报告进程状态
    def heartbeat_status(self):
        while self.bot.alive:
            time.sleep(600)
            # noinspection PyBroadException
            try:
                self.send_iter(self.groups_utils.admin_group(), self._status_text())
            except:
                # logger
                yield 'heartbeat status error'
                pass

    # @_admin_auth
    def server_mgmt(self, msg):
        """
        服务器管理:
            若消息文本为为远程命令，则执行对应函数
            若消息文本以 ! 开头，则作为 shell 命令执行
            若不满足以上，则尝试直接将 msg.text 作为 Python 代码执行
        """
        # 管理群内 判断是不是管理员的消息
        if self._from_admins(msg):
            order = self.remote_orders.get(msg.text.strip())
            if order:
                self._send_iter(msg.chat, order())
            elif msg.text.startswith('!'):
                command = msg.text[1:]
                self._send_iter(msg.chat, self._remote_shell(command))
            else:
                self._send_iter(msg.chat, self._remote_eval(msg.text))
