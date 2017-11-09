#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/4
import os
from setting import *
from wxpy import *


class Login(object):
    def __init__(self):
        self._cache_path = cache_path
        if not os.path.exists('./log'):
            os.system('mkdir ./log')
        self._console_qr = console_qr
        self.bot = None
        self._init_bot()

    def _init_bot(self):
        self.bot = Bot(
            cache_path=self._cache_path,
            console_qr=self._console_qr
        )

        # 为 True 时，将自动消除手机端的新消息小红点提醒
        self.bot.auto_mark_as_read = True
        self.bot.enable_puid(puid_path)
