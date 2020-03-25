#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'

import json

from gamecenter.api.base import BaseCorsHandler
from gamecenter.db import api as db_api
from gamecenter.sdk.game_sdk import sdk


class UserHandler(BaseCorsHandler):
    def get(self):
        uid, channel_id = self.get_uid_channel()
        user = db_api.user_get_by_uid_channel(uid, channel_id)

        if user is None:
            ret = sdk.get_user_info(uid, channel_id)
            if ret.get("code") == 0:
                user = {
                    "uid": ret.get("uid"),
                    "icon": ret.get("iconUrl"),
                    "channel_id": ret.get("channelId"),
                    "game_id": ret.get("gameId"),
                    "name": ret.get("name")
                }
                db_api.user_create(**user)
            else:
                self.write_error_message(400, "用户不存在%s" % uid)
        else:
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


class UserLogoutHandler(BaseCorsHandler):
    def get(self):
        uid, channel_id = self.get_uid_channel()

        ret = sdk.user_login_out(uid, channel_id)
        if ret.get("code") != 0:
            self.write_error_message(400, ret.get("msg"))

        ret = {
            "code": 200,
            "data": "success"
        }
        db_api.user_delete(uid, channel_id)

        self.write(ret)
