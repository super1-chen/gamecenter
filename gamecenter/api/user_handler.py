#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'

import json

from tornado.web import HTTPError

from gamecenter.api.base import BaseCorsHandler
from gamecenter.db import api as db_api


class UserHandler(BaseCorsHandler):

    def get(self):
        uid, channel_id = self.get_uid_channel()
        user = db_api.user_get_by_uid_channel(uid, channel_id)
        sdk = self.create_sdk()

        if user is None:
            resp_json = sdk.get_user_info(uid, channel_id)
            if resp_json.get("code") == 0:
                data = resp_json.get("data")
                if data is None:
                    raise HTTPError(status_code=400, reason=u"未找到用户")

                user = {
                    "uid": data.get("uid"),
                    "icon": data.get("iconUrl"),
                    "channel_id": data.get("channelId"),
                    "game_id": data.get("gameId"),
                    "name": data.get("name")
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
            "api_name": "get_user_info",
            "data": json.dumps(user)
        }

        self.write(ret)

    def post(self):
        uid, channel_id = self.get_uid_channel()
        data = self.get_json_body()

        name = data.get("name")
        game_id = data.get("game_id")
        icon_url = data.get("icon_url")

        if name is None:
            self.write_error_message(400, "缺少name")

        if game_id is None:
            self.write_error_message(400, "缺少game_id")

        if icon_url is None:
            self.write_error_message(400, "缺少icon_url")

        sdk = self.create_sdk()
        sdk.user_login(uid, name, channel_id, game_id, icon_url)

        ret = {
            "code": 200,
            "api_name": "post_user_info",
            "data": ""
        }

        self.write(ret)


class UserLogoutHandler(BaseCorsHandler):
    def get(self):
        uid, channel_id = self.get_uid_channel()
        sdk = self.create_sdk()

        ret = sdk.user_login_out(uid, channel_id)

        if ret.get("code") != 0:
            self.write_error_message(400, ret.get("msg"))

        ret = {
            "code": 200,
            "api_name": "user_logout",
            "data": ""
        }
        db_api.user_delete(uid, channel_id)

        self.write(ret)
