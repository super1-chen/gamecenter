#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'

import json
import logging
import time

from gamecenter.api.base import BaseCorsHandler
from gamecenter.mongodb import api as mongo_api

LOG = logging.getLogger(__name__)


class GameLogsHandler(BaseCorsHandler):
    def get(self):
        # room_id=1&game_id=1&start=13131313131&end=131313131
        # uid, channel = self.get_uid_channel()
        self.get_uid_channel()
        room_id = self.get_query_argument("room_id", None)
        start = self.get_query_argument("start", default=0)
        end = self.get_query_argument("end", default=None)

        if room_id is None:
            self.write_error_message(400, u"缺少参数room_id")

        if end is None:
            end = int(time.time())

        logs = mongo_api.get_game_logs(room_id, start, end)
        data = {"logs": logs}

        self.write(
            {
                "code": 200,
                "api_name": "get_game_logs",
                "data": json.dumps(data)
            }
        )

    def post(self):
        """
        fake_data = {
            "room_id": 1,
            "game_id": 1,
            "logs": "",
            "timestamp": 11313131,
            "player_id": 1
        }
        :return:
        """

        uid, channel = self.get_uid_channel()
        LOG.info("request body %s" % self.request.body)
        data = self.get_json_body()
        room_id = data.get("room_id")
        game_id = data.get("game_id")
        timestamp = data.get("timestamp")
        player_id = data.get("player_id")
        logs = data.get("logs")

        if room_id is None:
            self.write_error_message(400, u"缺少room_id")

        if game_id is None:
            self.write_error_message(400, u"缺少game_id")


        if player_id is None:
            self.write_error_message(400, u"player_id")


        if timestamp is None:
            timestamp = int(time.time())

        mongo_api.post_game_logs(timestamp, game_id, room_id, uid, channel, logs, player_id)

        self.write({
            "code": 200,
            "api_name": "post_game_logs",
            "data": "{}"
        })


class GameCurrentLogsHandler(BaseCorsHandler):
    def get(self):
        # room_id=1&game_id=1&start=13131313131&end=131313131
        # uid, channel = self.get_uid_channel()

        room_id = self.get_query_argument("room_id", None)
        game_id = self.get_query_argument("game_id", None)

        if room_id is None:
            self.write_error_message(400, u"缺少参数room_id")

        if game_id is None:
            self.write_error_message(400, u"缺少参数game_id")

        log = mongo_api.get_current_logs(game_id, room_id)

        if log is None:

            ret_log = {}

        else:
            ret_log = {
                "timestamp": log.time_stamp,
                "logs": log.logs,
                "player_id": log.player_id,
            }

        self.write(
            {
                "code": 200,
                "api_name": "get_current_game_logs",
                "data": json.dumps(ret_log)
            }
        )

    def post(self):
        """
        fake_data = {
            "room_id": 1,
            "game_id": 1,
            "logs": "",
            "timestamp": 11313131
        }
        :return:
        """

        uid, channel = self.get_uid_channel()
        LOG.info("request body %s" % self.request.body)
        data = self.get_json_body()
        room_id = data.get("room_id")
        game_id = data.get("game_id")
        player_id = data.get("player_id")
        timestamp = data.get("timestamp")
        logs = data.get("logs")

        if room_id is None:
            self.write_error_message(400, u"缺少room_id")

        if game_id is None:
            self.write_error_message(400, u"缺少game_id")

        if player_id is None:
            self.write_error_message(400, u"缺少player_id")

        if timestamp is None:
            timestamp = int(time.time())

        mongo_api.post_current_logs(timestamp, game_id, room_id, channel, logs, player_id)

        self.write({
            "code": 200,
            "api_name": "post_current_game_logs",
            "data": "{}"
        })


class GameListHandler(BaseCorsHandler):
    def get(self):
        self.get_uid_channel()
        sdk = self.create_sdk()
        req_json = sdk.get_games()
        data = req_json["data"]

        games = map(self._format_games, data)

        data = {"game_list": games}

        self.write({
            "code": 200,
            "api_name": "get_game_list",
            "data": json.dumps(data)
        })

    def _format_games(self, game):
        return {
            "desc": game["desc"],
            "icon": game["iconUrl"],
            "id": game["id"],
            "name": game["name"]
        }
