#!/usr/bin/env python3
# coding: utf-8
from wxpy import *
from timed_list import TimedList
import logging
import os
import re
import time



#--------------配置开始----------------

admin_puids = (
    #manue1
    '4ada2e0c',
    #蝌蚪
    '5a1d3905'
)
group_puids = (
    # 豪情
    '2444b6a7',
    #564
    '4fe94bb7'
)
# 测试群564
test_group_puid = '4fe94bb7'

# 管理群
# 仅为一个，用于接收心跳上报等次要信息
# admins 564
admin_group_puid = '4fe94bb7'

# 自动回答关键词
kw_replies = {
    '个人主页:\nwww.manue1.site': (
        '项目', '主页', '官网', '网站', 'github', '地址', 'repo', '版本'
    ),
    'my blog:\nwww.manue1.site': (
        '请问', '文档', '帮助', '怎么', '如何', '请教', '安装', '说明', '运行'
    ),
    '必看: 常见问题 FAQ:\nwww.manue1.site': (
        'faq', '常见', '问题', '问答', '什么'
    ),
    '@fil@{}'.format(__file__): (
        '源码', '代码'
    )
}
# 新人入群的欢迎语
welcome_text = '''🎉 欢迎 @{} 的加入！'''

help_info = '''😃 讨论主题
· 不限制其他话题，请区分优先级
· 支持分享对群员有价值的信息

⚠️ 注意事项
· 严禁灰产/黑产相关内容话题
· 请勿发布对群员无价值的广告

👮 投票移出
· 移出后将被拉黑 24 小时
· 请在了解事因后谨慎投票
· 命令格式: "移出 @人员"
'''

#---------------配置结束--------------------

bot = Bot(cache_path="/tmp/wxpy_cache",console_qr=1) 
bot.enable_puid('puidtest.pkl')

gs = bot.groups(update=True).search()
for g in gs :
    print(g,g.puid)

groups = list(map(lambda x: bot.groups().search(puid=x)[0], group_puids))
print(groups)
test_group = bot.groups().search(puid=test_group_puid)[0]

# 初始化聊天机器人
tuling = Tuling(api_key='61eea024ed154d8f9d8a33e98547057a')


# 判断消息是否为支持回复的消息类型
def supported_msg_type(msg, reply_unsupported=False):
    supported = (TEXT,)
    ignored = (SYSTEM, NOTE, FRIENDS)

    fallback_replies = {
        RECORDING: '🙉',
        PICTURE: '🙈',
        VIDEO: '🙈',
    }
    if msg.type in supported:
        return True
    elif (msg.type not in ignored) and reply_unsupported:
        msg.reply(fallback_replies.get(msg.type, '🐒'))



# 响应好友消息
@bot.register(Friend)
def exist_friends(msg):
    if supported_msg_type(msg, reply_unsupported=True):
        tuling.do_reply(msg)

# 在其他群中回复被 @ 的消息
@bot.register(Group, TEXT)
def reply_other_group(msg):
    if msg.chat not in groups and msg.is_at:
        if supported_msg_type(msg, reply_unsupported=True):
            tuling.do_reply(msg)

# wxpy 群的消息处理
@bot.register(groups, TEXT, except_self=False)
def wxpy_group(msg):
    #kick_msg = remote_kick(msg)
    if msg.text.lower().strip() == "hello":
        return "你是不是sb"
    elif msg.text.lower().strip() in ('帮助', '说明', '规则', 'help', 'rule', 'rules'):
        return help_info
    elif msg.is_at:
        return 'oops…\n干嘛呀[撇嘴]\n想我就私聊呗[害羞]'


@bot.register(test_group)
def forward_test_msg(msg):
    if msg.type is TEXT:
        ret = wxpy_group(msg)
        if ret:
            return ret
        elif msg.text.lower().strip() == 'test':
            return 'Hello!'
        elif msg.text == 'at':
            return 'Hello @{} !'.format(msg.member.name)

#embed()
bot.join()
