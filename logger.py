#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/6
import logging


class Logger(object):

    def get_logger(level=logging.DEBUG, file='bot.log', mode='a'):
        log_formatter = logging.Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
        log_formatter_lite = logging.Formatter('%(name)s:%(levelname)s:%(message)s')

        _logger = logging.getLogger()

        for hdlr in _logger.handlers:
            _logger.removeHandler(hdlr)

        # 输出到文件
        if file:
            file_hdlr = logging.FileHandler(file, mode)
            file_hdlr.setFormatter(log_formatter)
            _logger.addHandler(file_hdlr)

        # 输出到屏幕
        console_hdlr = logging.StreamHandler()
        console_hdlr.setLevel(logging.INFO)
        console_hdlr.setFormatter(log_formatter)
        _logger.addHandler(console_hdlr)

        # 输出到远程管理员微信
        wechat_hdlr = WeChatLoggingHandler(admins[0])
        wechat_hdlr.setLevel(logging.WARNING)
        wechat_hdlr.setFormatter(log_formatter_lite)
        _logger.addHandler(wechat_hdlr)

        # 将未捕捉异常也发送到日志中

        def except_hook(*args):
            logger.critical('UNCAUGHT EXCEPTION:', exc_info=args)
            _restart()

        sys.excepthook = except_hook

        for m in 'requests', 'urllib3':
            logging.getLogger(m).setLevel(logging.ERROR)

        _logger.setLevel(level)
        return _logger