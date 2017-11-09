#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/4
import random
from collections import Counter

import time
from wxpy import ensure_one

from setting import *
from utils.times import Time


class Groups(object):
    '''
        1.创建管理群 报编码错误
        2.邀请入群
    '''

    def __init__(self, bot):
        self.bot = bot
        self.groups = self.bot.groups(update=True)

        # 计算每个用户被邀请的次数
        self.invite_counter = Counter()

    # 添加想有群内所有人为好友
    def add_group_member(self):
        for group in self.groups:
            group.update_group(members_details=True)
            for user in group.member:
                if not user.is_friend:
                    yield u'开始尝试添加群{group_name}内的{member_name}为好友'.format(
                        group_name=group.name,
                        member_name=user.name
                    )
                    time.sleep(random.randrange(5, 20))
                    new_friend = user.add(verify_content=add_member_verify_content)
                    new_name = Time().str_20171105() + '-' + str(random.randint(1, 1000))
                    new_friend.set_remark_name(new_name)
                    yield u'添加群{group_name}内的{member_name}为好友成功'.format(
                        group_name=group.name,
                        member_name=user.name
                    )

    # 创建新群
    def create_group(self, users, topic):
        new_group = self.bot.create_group(users=users, topic=topic)
        return new_group

    # 关键字查找groups
    def search_group(self, key_word):
        return ensure_one(self.groups.search(keywords=key_word))

    # 获取管理群组的quid
    # def _group_puids(self):
    #     group_puids_list = []
    #     for group_name in groups_name:
    #         group_puids_list.append(self.search_group(group_name).puid)
    #     return group_puids_list

    # 通过puid 获取groups
    # def admin_groups(self):
    #     groups = []
    #     group_puids = self._group_puids()
    #     for puid in group_puids:
    #         groups.append(ensure_one(self.groups.search(puid=puid)))
    #     return groups

    # 获取user groups
    def user_groups(self):
        groups = []
        for group_name in groups_name:
            groups.append(self.search_group(group_name))

        return groups

    # 获取管理群
    def admin_group(self):
        return self.search_group(admin_group_name)

    # 自动选择未满的群
    def _min_group(self):
        groups = self.user_groups()
        groups.sort(key=len, reverse=True)
        for _group in groups:
            if len(_group) < 30:
                return _group
        else:
            return groups[-1]

    # 邀请入群
    def invite_group(self, user):
        groups = self.user_groups()
        joined = list()
        for group in groups:
            if user in group:
                joined.append(group)
        if joined:
            joined_nick_names = '\n'.join(map(lambda x: x.nick_name, joined))
            user.send(u'你已加入了\n{}'.format(joined_nick_names))
        else:
            group = self._min_group()
            user.send(u'验证通过 [嘿哈]')
            group.add_members(user, use_invitation=True)
            if self.invite_counter.get(user, 0) < invite_times_max:
                self.invite_counter.update([user])
            else:
                user.send(u'你的受邀次数已达最大限制 😷')
