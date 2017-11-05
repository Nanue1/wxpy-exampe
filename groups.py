#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/4
from wxpy import ensure_one

from setting import *


class Groups(object):
    '''
        1.创建管理群 报编码错误
        2.邀请入群
    '''

    def __init__(self, bot):
        self.bot = bot
        self.groups = self.bot.groups(update=True)

    # 创建新群
    def create_group(self, users, topic):
        new_group = self.bot.create_group(users=users, topic=topic)
        return new_group

    # 关键字查找groups
    def _search_group(self, key_word):
        return ensure_one(self.groups.search(keywords=key_word))

    # 获取管理群组的quid
    # def _group_puids(self):
    #     group_puids_list = []
    #     for group_name in groups_name:
    #         group_puids_list.append(self._search_group(group_name).puid)
    #     return group_puids_list

    # 通过puid 获取groups
    # def admin_groups(self):
    #     groups = []
    #     group_puids = self._group_puids()
    #     for puid in group_puids:
    #         groups.append(ensure_one(self.groups.search(puid=puid)))
    #     return groups

    # 获取admin groups
    def _admin_groups(self):
        groups = []
        for group_name in groups_name:
            groups.append(self._search_group(group_name))

        return groups

    # 自动选择未满的群
    def _min_group(self):
        groups = self._admin_groups()
        groups.sort(key=len, reverse=True)
        for _group in groups:
            if len(_group) < 30:
                return _group
        else:
            return groups[-1]

    # 邀请入群
    def invite_group(self, user):
        groups = self._admin_groups()
        joined = list()
        for group in groups:
            if user in group:
                joined.append(group)
        if joined:
            joined_nick_names = '\n'.join(map(lambda x: x.nick_name, joined))
            # logger.info('{} is already in\n{}'.format(user, joined_nick_names))
            user.send(u'你已加入了\n{}'.format(joined_nick_names))
        else:
            group = self._min_group()
            user.send(u'验证通过 [嘿哈]')
            group.add_members(user, use_invitation=True)

