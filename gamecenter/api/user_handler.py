#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'
import json

from gamecenter.api.base import BaseCorsHandler
from gamecenter.db import api as db_api


class UserHandler(BaseCorsHandler):
    def get(self):
        uid, channel_id = self.get_uid_channel()
        user = db_api.find_user(uid, channel_id)

        user = {
            "uid": user.uid,
            "icon": user.icon,
            "channel_id": user.channel,
            "game_id": 1,
            "name": user.name
        }

        ret = {
            "code": 200,
            "data": json.dumps(user)
        }
        self.write(ret)
