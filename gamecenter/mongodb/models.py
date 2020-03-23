#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'
import time

from mongoengine import Document
from mongoengine import StringField
from mongoengine import IntField


class GameLogs(Document):
    # 是游戏平台穿过来的id
    uid = StringField(max_length=32, required=True)
    time_stamp = IntField(default=lambda: int(time.time()))
    room_id = IntField(default=1)
    game_id = IntField(default=1)
    channel_id = StringField(max_length=1024)
    logs = StringField(max_length=2048, default="")

    meta = {
        'db_alias': 'gamecenter',
        'indexes': [
            "time_stamp",
            "room_id",
        ],
        'ordering': ['+time_stamp']
    }