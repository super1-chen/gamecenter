#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'
import logging

from mongoengine import connect

from gamecenter import cfg
from gamecenter.mongodb import models

LOG = logging.getLogger(__name__)


def init_mongo_connection():
    host = cfg.config().get("MONGODB", 'mongodb_url')

    LOG.debug('start mongodb @ %(host)s' % {"host": host})
    connect("gamecenter", "gamecenter", host=host)


def post_game_logs(timestamp, game_id, room_id, uid, channel_id, logs, player_id=1):
    log = models.GameLogs(
        uid=uid,
        time_stamp=timestamp,
        room_id=room_id,
        game_id=game_id,
        logs=logs,
        channel_id=channel_id,
        player_id=player_id
    )
    log.save()


def get_game_logs(room_id, start, end):
    logs = models.GameLogs.objects.filter(
        room_id=room_id,
        time_stamp__gt=start,
        time_stamp__lte=end,
    )
    ret = []
    for log in logs:
        ret.append(
            {
                "timestamp": log.time_stamp,
                "uid": log.uid,
                "channel_id": log.channel_id,
                "player_id": log.player_id,
                "logs": log.logs
            }
        )
    return ret


def delete_game_logs(deadline):
    """
    delete date by end line

    :param deadline: timestamp of deadline
    :type deadline: int
    :return:
    """
    models.GameLogs.objects.filter(time_stamp__lte=deadline).delete()


def post_current_logs(timestamp, game_id, room_id, channel_id, logs, player_id):
    log = models.GameCurrentLogs.objects.filter(
        room_id=room_id, game_id=game_id).first()

    kwargs = dict(
        time_stamp=timestamp,
        game_id=game_id,
        room_id=room_id,
        channel_id=channel_id,
        logs=logs,
        player_id=player_id
    )

    if log:
        log.update(**kwargs)
    else:
        log = models.GameCurrentLogs(**kwargs)
        log.save()


def get_current_logs(game_id, room_id):
    return models.GameCurrentLogs.objects.filter(room_id=room_id, game_id=game_id).first()

