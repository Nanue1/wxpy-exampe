#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/11/4
import datetime
import time
import os
import subprocess
import sys
from pprint import pformat
import psutil
from wxpy import Group
from wxpy.utils import start_new_thread

from friends import Friends
from groups import Groups
from logger import Logger
from utils.tumblr import Tumblr


class Commands(object):
    '''
    1. 远程重启
    2.TODO定时任务
    '''

    def __init__(self, bot):
        self.bot = bot
        self.logger = Logger(bot).init_logger()
        self.process = psutil.Process()
        self.friends_utils = Friends(bot)
        self.groups_utils = Groups(bot)

        # 远程命令 (单独发给机器人的消息)
        self.remote_orders = {
            'gu': self._update_groups,
            'ga': self._add_group_member,
            's': self._status_text,
            'r': self._restart,
            'l': self._latency,
            'p': self._send_tumblr_picture,
            'v': self._send_tumblr_video,
        }

    # 添加所有群内所有人为好友
    def _add_group_member(self):
        try:
            start_new_thread(self.groups_utils.add_group_member())
        except Exception as e:
            self.logger.exception('failed to report heartbeat:\n {}',e)

    def _send_tumblr_picture(self):
        Tumblr(self.bot).send_tumblr_picture(),
        yield 'tumblr pic send done.'

    def _send_tumblr_video(self):
        pass

    def _from_admins(self, msg):
        """
        判断 msg 的发送者是否为管理员
        """
        from_user = msg.member if isinstance(msg.chat, Group) else msg.sender
        return from_user in self.friends_utils.admin_friends()

    @staticmethod
    def _send_iter(receiver, iterable):
        """
        用迭代的方式发送多条消息
        :param receiver: 接收者
        :param iterable: 可迭代对象
        """
        print type(iterable)
        if isinstance(iterable, str):
            raise TypeError
        for msg in iterable:
            receiver.send(msg)

    def _remote_shell(self, command):
        self.logger.info('executing remote shell cmd:\n{}'.format(command))
        r = subprocess.Popen(
            command, shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            universal_newlines=True
        )
        if r.stdout:
            yield ' '.join(r.stdout.readlines())

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
            _group.update_group(members_details=True)
            yield '{}: {}'.format(_group.name, len(_group))

    def _restart(self):
        yield 'restarting bot...'
        self.bot.dump_login_status()
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
                self.logger.info('executing remote order: {}'.format(order.__name__))
                self._send_iter(msg.chat, order())
                # TODO
            elif msg.text.startswith(u'!'):
                command = msg.text[1:]
                self._send_iter(msg.chat, self._remote_shell(command))
            else:
                self._send_iter(msg.chat, self._remote_eval(msg.text))

                # 定时报告进程状态

    def heartbeat(self):
        while self.bot.alive:
            time.sleep(600)
            # noinspection PyBroadException
            try:
                self._send_iter(self.groups_utils.admin_group(), self._status_text())
            except:
                self.logger.exception('failed to report heartbeat:\n')
