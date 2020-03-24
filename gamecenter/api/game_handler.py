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
            self.write_error_message(400, "缺少参数room_id")

        if end is None:
            end = int(time.time())

        logs = mongo_api.get_game_logs(room_id, start, end)

        self.write(
            {
                "code": 200,
                "logs": json.dumps(logs)
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
        timestamp = data.get("timestamp")
        logs = data.get("logs")

        if room_id is None:
            self.write_error_message(400, "缺少room_id")

        if game_id is None:
            self.write_error_message(400, "缺少game_id")

        if timestamp is None:
            timestamp = int(time.time())

        mongo_api.post_game_logs(timestamp, game_id, room_id, uid, channel, logs)

        self.write({
            "code": 200,
            "data": "{}"
        })


class GameCurrentLogsHandler(BaseCorsHandler):
    def get(self):
        # room_id=1&game_id=1&start=13131313131&end=131313131
        # uid, channel = self.get_uid_channel()

        room_id = self.get_query_argument("room_id", None)
        game_id = self.get_query_argument("game_id", None)

        if room_id is None:
            self.write_error_message(400, "缺少参数room_id")

        if game_id is None:
            self.write_error_message(400, "缺少参数game_id")

        log = mongo_api.get_current_logs(game_id, room_id)

        if log is None:
            return {}

        else:
            ret_log = {
                "timestamp": log.time_stamp,
                "logs": log.logs
            }

        self.write(
            {
                "code": 200,
                "logs": json.dumps(ret_log)
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
        timestamp = data.get("timestamp")
        logs = data.get("logs")

        if room_id is None:
            self.write_error_message(400, "缺少room_id")

        if game_id is None:
            self.write_error_message(400, "缺少game_id")

        if timestamp is None:
            timestamp = int(time.time())

        mongo_api.post_current_logs(timestamp, game_id, room_id, channel, logs)

        self.write({
            "code": 200,
            "data": "{}"
        })
