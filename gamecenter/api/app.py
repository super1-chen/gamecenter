#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22
from __future__ import absolute_import

import json
import logging

import tornado
import tornado.httpserver
import tornado.ioloop
import tornado.options
import tornado.web


from gamecenter.api import game_handler
from gamecenter.api import room_handler
from gamecenter.api import user_handler
from gamecenter.api import error_handler
from gamecenter.api import main_handler

LOG = logging.getLogger(__name__)

# pattern part
URL_PREFIX = r"/v1/gamecenter"

main_pattern = [
    (r"/v1", main_handler.MainHandler),
]

user_patterns = [
    (URL_PREFIX + r"/user_info", user_handler.UserHandler),
    (URL_PREFIX + r"/user_logout", user_handler.UserLogoutHandler),
]

game_patters = [
    (URL_PREFIX + r"/game_logs", game_handler.GameLogsHandler),
    (URL_PREFIX + r"/game_current_logs", game_handler.GameCurrentLogsHandler),
    (URL_PREFIX + r"/game_list", game_handler.GameListHandler)
]

room_patterns = [
    (URL_PREFIX + r"/room_list", room_handler.RoomListHandler),
    (URL_PREFIX + r"/room", room_handler.RoomHandler),
    (URL_PREFIX + r"/room/(\d+)", room_handler.RoomHandler),
    (URL_PREFIX + r"/join_room", room_handler.RoomJoinHandler),
    (URL_PREFIX + r"/quit_room", room_handler.RoomQuitHandler),
    (URL_PREFIX + r"/room/(\d+)", room_handler.RoomHandler),
    (URL_PREFIX + r"/game_over", room_handler.GameOverHandler),
    (URL_PREFIX + r"/game_start", room_handler.GameStartHandler),
]

url_patterns = user_patterns +\
               game_patters + \
               main_pattern +\
               room_patterns


class WebApp(tornado.web.Application):
    def __init__(self, debug=False):
        handlers = url_patterns
        setting = dict(debug=debug, default_handler_class=error_handler.NotFoundHandler)
        tornado.web.Application.__init__(
            self, handlers, autoreload=True, **setting
        )


def run_api(mode, port=8000, address="127.0.0.1"):
    LOG.info(mode)
    http_server = tornado.httpserver.HTTPServer(WebApp(debug=mode))
    http_server.listen(port, address)
    LOG.info('start run at %s:%s ' % (address, port))
    tornado.ioloop.IOLoop.current().start()
