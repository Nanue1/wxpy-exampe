#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/4


# Bot init 缓存路径，可以避免短时间内二次扫码
cache_path = './log/cache_bot.pkl'

# puid 缓存位置
puid_path = './log/puid_bot.pkl'

# Bot 对象初始化时的 console_qr 参数值
console_qr = 2.5

# 入群口令
group_code = u'嘿哈'

# 添加好友验证信息关键字
auto_accept_msg_keyword = u'嘿哈'

# 新添加好友提示语
new_friend_text = u'''
    你好,我们已经是朋友了
    入群，请输入口令:嘿哈
'''

# 需管理的微信群
# 可为多个，机器人必须为群主，否则无法执行相应操作
groups_name = [u'豆瓣灌水@_@', u'豆瓣灌水=_=']


# 管理员，可为多个，用于执行管理
# 首个管理员为"系统管理员"，可接收异常日志和执行服务端操作
# 其他管理员仅执行微信群管理
admin_mangers_name = ['Yune1', 'Funy', 'manue1']

# 管理群
# 仅为一个，用于接收心跳上报等次要信息
# 开发测试 admins
admin_group_name = '开发测试'
# 自动回答关键词
kw_replies = {
    '入群口令为:嘿哈': (
        '口令', '暗号', '豆瓣', '发车', '上车'
    ),
}

# 新人入群的欢迎语
welcome_text = u'''
               🎉 欢迎 @{} 的加入!
               新人讲一下你的故事
               否则群员可投票把你踢
               出奥.
               '''

help_info = '''😃 讨论主题
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
