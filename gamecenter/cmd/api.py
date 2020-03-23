#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'
import argparse
import datetime
import json

import tornado
from tornado.options import define

from gamecenter import cfg
from gamecenter import log
from gamecenter.api import app
from gamecenter.mongodb import api as mongo_api
from gamecenter import utils

DT_HANDLER = lambda obj: obj.strftime("%Y-%m-%d %H:%M:%S") \
    if isinstance(obj, datetime.datetime) \
       or isinstance(obj, datetime.date) else None

def json_encode(value):
    return json.dumps(value, default=DT_HANDLER).replace("</", "<\/")


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-p', '--port', default=8000, type=int,
                        help="run on the give port")
    parser.add_argument('-a', '--address', default="127.0.0.1", type=str,
                             help="run on the give address")

    parser.add_argument('-c', '--config', help='use specific config file')
    args = parser.parse_args()

    if args.config:
        cfg.load_config(args.config)
    else:
        cfg.load_config()

    log.setup()

    mode = cfg.config().getboolean("DEFAULT","debug")

    mongo_api.init_mongo_connection()

    tornado.escape.json_encode = json_encode

    app.run_api(mode, args.port, args.address)