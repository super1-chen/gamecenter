#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-26

__author__ = 'Albert'

import logging
import time

from gamecenter import cfg
from gamecenter.worker.base import crontab
from gamecenter.worker.base import my_async
from gamecenter.mongodb import api

LOG = logging.getLogger(__name__)


@my_async.periodic_task(crontab(minute='0', hour='*', day='*'))
def delete_old_game_logs():
    key_hours = cfg.config().get_int("OLD_DATA", "keep_hour")

    api.init_mongo_connection()
    dead_line = int(time.time()) - 3600 * key_hours
    api.delete_game_logs(dead_line)
