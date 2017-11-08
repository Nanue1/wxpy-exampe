#!/usr/bin/env python
# -*- coding: utf-8 -*-   
# Created by manue1 on 2017/11/8
import json
import os
from setting import *
from groups import Groups
import random

import time


class Tumblr(object):
    def __init__(self, bot):
        self.groups_util = Groups(bot)
        self.target = self.groups_util.search_group(tumblr_target_group)

    def send_tumblr_picture(self):
        i = 0
        for pic in os.listdir(tumblr_picture_path):
            i += 1
            if i < 50:
                pic_path = tumblr_picture_path + pic
                self.target.send(u'share pic %s ' % i)
                time.sleep(random.randrange(1,3))
                file_data = self.target.send_image(pic_path)
                with open(tumblr_pic_media_id_path,'a') as f:
                    f.write(json.dumps(file_data + '\n'))
                # cmd = "rm -f %s" % pic_path
                # os.system(cmd)
                time.sleep(random.randrange(3,5))
            else:
                break
