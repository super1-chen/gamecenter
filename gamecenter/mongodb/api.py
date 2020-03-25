#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'
import logging

from mongoengine import connect
from pymongo import ReadPreference

from gamecenter import cfg
from gamecenter.mongodb import models

LOG = logging.getLogger(__name__)


def init_mongo_connection():
    address = cfg.config().get("MONGODB", 'address')
    # username = cfg.config().get("MONGODB",'username', raw=True)
    # password = cfg.config().get("MONGODB", 'password', raw=True)
    # megset = cfg.config().get("MONGODB", 'megset', raw=True)

    username = None
    password = None
    megset = None

    host = address.split(',')
    LOG.debug('start mongodb @ %(host)s' % {"host": address})
    if len(host) > 1:
        connect(
            'gamecenter', 'gamecenter',
            host=host,
            replicaset=megset,
            username=username,
            password=password,
            authentication_source='admin',
            read_preference=ReadPreference.SECONDARY,
            connect=False
        )
    else:
        connect(
            'gamecenter', 'gamecenter',
            host=host,
            username=username,
            password=password,
            authentication_source='admin',
            connect=False
        )


def post_game_logs(timestamp, game_id, room_id, uid, channel_id, logs):
    log = models.GameLogs(
        uid=uid,
        time_stamp=timestamp,
        room_id=room_id,
        game_id=game_id,
        logs=logs,
        channel_id=channel_id
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
                "logs": log.logs
            }
        )
    return ret


def post_current_logs(timestamp, game_id, room_id, channel_id, logs):
    log = models.GameCurrentLogs.objects.filter(
        room_id=room_id, game_id=game_id).first()

    kwargs = dict(
        time_stamp=timestamp,
        game_id=game_id,
        room_id=room_id,
        channel_id=channel_id,
        logs=logs
    )

    if log:
        log.update(**kwargs)
    else:
        log = models.GameCurrentLogs(**kwargs)
        log.save()


def get_current_logs(game_id, room_id):
    return models.GameCurrentLogs.objects.filter(room_id=room_id, game_id=game_id).first()
