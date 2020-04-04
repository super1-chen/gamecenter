#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-24

__author__ = 'Albert'

import json

from gamecenter.api.base import BaseCorsHandler
from gamecenter.db import api as db_api
from gamecenter.exception import GameHttpError


def _format_room(room_qset):
    room = {
        "id": room_qset.id,
        "people": room_qset.people,
        "participators": len(room_qset.users),
        "status": room_qset.status,
        "start_time": room_qset.start_time
    }
    return room


class RoomListHandler(BaseCorsHandler):
    def get(self):
        self.get_uid_channel()
        game_id = self.get_game_id()

        records = db_api.room_list_get_game_id(game_id)
        rets = []
        for r in records:
            ret = _format_room(r)

            rets.append(ret)

        room_list = {"room_list": rets}

        data = {
            "code": 0,
            "api_name": "get_room_list",
            "data": json.dumps(room_list)
        }

        self.write(data)


class RoomHandler(BaseCorsHandler):

    def get(self, room_id):
        self.get_uid_channel()
        room = db_api.room_get_by_id(room_id)
        if room is None:
            raise GameHttpError(400, u"room %s 不存在" % room_id)

        ret = _format_room(room)

        data = {
            "code": 0,
            "api_name": "get_room",
            "data": json.dumps(ret)
        }
        self.write(data)

    def post(self):
        uid, channel_id = self.get_uid_channel()
        data = self.get_json_body()

        game_id = data.get("game_id", None)
        people = data.get("people", None)

        if game_id is None:
            self.write_error_message(400, u"缺少参数game_id")
        if people is None:
            self.write_error_message(400, u"缺少参数people")

        room = db_api.room_create_by_game(game_id, uid, channel_id, people)

        ret = _format_room(room)

        data = {
            "code": 0,
            "api_name": "create_room",
            "data": json.dumps(ret)
        }
        self.write(data)

    def delete(self, room_id):
        uid, channel_id = self.get_uid_channel()
        db_api.delete_room(uid, channel_id, room_id)

        data = {
            "code": 0,
            "api_name": "delete_room",
            "data": json.dumps({})
        }

        self.write(data)


class RoomJoinHandler(BaseCorsHandler):
    def post(self):
        uid, channel_id = self.get_uid_channel()
        data = self.get_json_body()

        room_id = data.get("room_id", None)

        if room_id is None:
            self.write_error_message(400, u"缺少参数room_id")

        db_api.user_join_room(room_id, uid, channel_id)

        data = {
            "code": 0,
            "api_name": "join_game",
            "data": json.dumps({})
        }
        self.write(data)


class RoomQuitHandler(BaseCorsHandler):
    def post(self):
        uid, channel_id = self.get_uid_channel()

        db_api.user_quite_room(uid, channel_id)

        data = {
            "code": 0,
            "api_name": "quit_game",
            "data": json.dumps({})
        }
        self.write(data)


class GameStartHandler(BaseCorsHandler):
    def post(self):
        uid, channel_id = self.get_uid_channel()

        data = self.get_json_body()

        room_id = data.get("room_id", None)

        if room_id is None:
            self.write_error_message(400, u"缺少参数room_id")

        db_api.start_game(uid, channel_id, room_id)

        data = {
            "code": 0,
            "api_name": "game_start",
            "data": json.dumps({"int": 2})
        }
        self.write(data)


class GameOverHandler(BaseCorsHandler):
    def post(self):
        uid, channel_id = self.get_uid_channel()

        data = self.get_json_body()

        room_id = data.get("room_id", None)

        if room_id is None:
            self.write_error_message(400, u"缺少参数room_id")

        db_api.end_game(uid, channel_id, room_id)

        data = {
            "code": 0,
            "api_name": "game_over",
            "data": json.dumps({})
        }
        self.write(data)
