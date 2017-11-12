#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Created by manue1 on 2017/11/4


# Bot init 缓存路径，可以避免短时间内二次扫码
cache_path = './log/cache_bot.pkl'

# puid 缓存位置
puid_path = './log/puid_bot.pkl'

# log 日志位置
log_path = './log/bot.log'

# Bot 对象初始化时的 console_qr 参数值
console_qr = 2

# 登陆的用户
bot_user_name = u'Yune1'
# 三个好友，用于初始化下面群组,没有群组的话会自动创建
users_name = [bot_user_name, u'Funy', u'manue1']

# 管理员，可为多个，用于执行管理
# 首个管理员为"系统管理员"，可接收异常日志和执行服务端操作
# 其他管理员仅执行微信群管理
admin_mangers_name = [u'Funy', u'Yune1', u'manue1']

# 管理群
admin_group_name = u'开发测试'

# 需管理的微信群
# 可为多个，机器人必须为群主，否则无法执行相应操作
douban_groups_name = [u'豆瓣灌水@_@', u'豆瓣灌水=_=']
mahjong_groups_name = [u'欢乐麻将@_@', u'欢乐麻将=_=']
king_groups_name = [u'稳住别浪@_@', u'稳住别浪=_=']
werewolf_groups_name = [u'天黑请闭眼@_@', u'天亮请睁眼=_=']
sex_groups_name = [u'Nude_chat@_@', u'Nude_chat=_=']

# 管理的所有群组，需要初始化
all_groups_name = douban_groups_name + \
                  mahjong_groups_name + \
                  king_groups_name + \
                  werewolf_groups_name + \
                  sex_groups_name
all_groups_name.append(admin_group_name)

# 入群口令
group_codes = {u'嘿哈': douban_groups_name,
               u'麻将': mahjong_groups_name,
               u'稳住': king_groups_name,
               u'狼人': werewolf_groups_name,
               u'nude': sex_groups_name}

# 自动回答关键词
keyword_replies = {
    u'还记得我们的入群口令吗?': (
        u'豆瓣', u'发车', u'上车', u'进群', u'入群'
    ),
}

# 机器人 api
api_key = '61eea024ed154d8f9d8a33e98547057a'

# 最大邀请测试
invite_times_max = 2

# tumblr data path
tumblr_picture_path = '/root/scrapy_tumblr/tumblr_picture/picture/full/'
tumblr_video_path = ''
tumblr_target_group = u'豆瓣灌水@_@'
tumblr_pic_media_id_path = './log/tumblr_pic_media_id'

# 添加群成员 验证信息
add_member_verify_content = u'你好,可以让臣妾陪你聊一会吗^_^'
# 新人入群的欢迎语
welcome_text = u'''
               🎉 欢迎 @{} 的加入!
               新人讲一下你的故事
               否则群员可投票把你踢
               出奥.
               '''

help_info = u'''😃 讨论主题
· 群内不限制聊天话题
· 支持分享对群员有价值的信息
· 22点后,可发车
⚠️ 注意事项
· 新成员入群，需讲述一个秘密
   (自己/他人)
· 秘密描述不得少于50字
· 不说秘密者，可投票移出
👮 投票移出
· 移出后将被拉黑 24 小时
· 请在了解事因后谨慎投票
· 命令格式: "移出 @人员"
'''
