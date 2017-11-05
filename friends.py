#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/4
import random
import re

import time
import traceback

from wxpy import ensure_one

from utils.times import Time
from setting import *


class Friends(object):
    '''
    1. 统计好友总量
    2. 按条件分类统计好友
    3. 按条件列出好友
    4. 添加好友
    5. 按备注分类用户组
    6. 全部好友设置备注
    '''

    def __init__(self, bot):
        self.bot = bot
        self.friends = self.bot.friends(update=True)

    # 好友数
    def friends_count(self):
        return len(self.friends)

    # 所有好友
    def all_friends_name(self):
        puid_name_list = []
        for friends in self.friends:
            puid_name_list.append({'puid': friends.puid, 'name': friends.name})
        return puid_name_list

    # 男女个数
    def sex_friends(self):
        boy_count = 0
        girl_count = 0
        for friends in self.friends:
            if friends.sex == 1:
                boy_count += 1
            else:
                girl_count += 1
        return {'boy': boy_count, 'girl': girl_count}

    # 条件搜索
    def _search_friend(self, key_word):

        return ensure_one(self.friends.search(keywords=key_word))

    # 20171105-nick_name 备注分组返回用户
    def remark_name_search(self):
        remark_name_friends = []
        for friends in self.friends:
            remark_name = friends.remark_name
            if re.match('^\d{6,8}-', remark_name):
                remark_name_friends.append(friends)
            else:
                pass
        return remark_name_friends

    # 部分好友昵称乱码 全部重新设置昵称
    def rename_users(self):
        for friend in self.friends:
            try:
                time.sleep(random.randint(10, 15))
                remark_name = friend.remark_name
                if not re.match('^\d{6,8}-', remark_name):
                    new_name = Time().str_20171105() + '-' + str(random.randint(1, 1000))
                    friend.set_remark_name(new_name)
                    print friend.remark_name + '\t' + friend.nick_name
                else:
                    pass
            except:
                traceback.print_exc()
                continue

    # 获取管理员的puids
    def admin_puids(self):
        admin_puids_list = []
        for admin_name in admin_mangers_name:
            admin_puids_list.append(self._search_friend(admin_name).puid)
        return admin_puids_list
