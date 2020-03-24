#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2017年 陈超. All rights reserved by Chao.Chen.
# Create on 2017-08-09
from __future__ import absolute_import
import urllib
import json
import logging

import tornado.web

logger = logging.getLogger('__name__')


class BaseHandler(tornado.web.RequestHandler):
    """
    A class to collect common handler methods - all other handlers should
    subclass this one.
    """

    def load_json(self):
        """
        Load JSON from the request.body and store them in self.request.arguments,
        like tornado  does by default for POSTed form parameters
        :return:
        """
        try:
            self.request.arguments = json.loads(self.request.body)
        except ValueError:
            msg = "Could not decode Json: %s " % self.request.body
            logger.debug(msg)
            raise tornado.web.HTTPError(400, msg)

    def get_json_argument(self, name, default=None):
        """
        Find and return the argument with key 'name' from JSON request data.
        Similar to Tornado's get_argument() method. If default is None will raise HTTPError
        :param name: argument name
        :param default: default value
        :return:
        """

        if default is None:
            default = self._ARG_DEFAULT
        if not self.request.arguments:
            self.load_json()

        if name not in self.request.arguments:
            if default is self._ARG_DEFAULT:
                msg = "Missing argument '%s'" % name
                logger.debug(name)
                raise tornado.web.HTTPError(400, msg)

            logger.debug("Returning default argument %s, as we"
                         " couldn't find '%s' in %s" % (
                         default, name, self.request.arguments))

            return default
        arg = self.request.arguments[name]
        logger.debug("Found %s: %s in JSON argument" % (name, arg))
        return arg


class BaseCorsHandler(BaseHandler):
    def set_default_headers(self):
        self.set_header('Access-Control-Allow-Credentials', 'false')
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header("Content-Type", "application/json")
        self.set_header(
            'Access-Control-Allow-Headers',
            'x-requested-with, Authentication-token, '
            'Content-Type, Accept, Accept-Language,'
            ' Content-Language'
        )
        self.set_header('Access-Control-Allow-Methods',
                        'POST,GET,PUT,DELETE,OPTIONS')

    def options(self):
        # no body
        self.set_status(204)
        self.finish()

    def get_current_user(self):
        user_id = 1
        if user_id:
            return user_id
        else:
            return None

    def write_error(self, *args, **kwargs):
        err_cls, err, traceback = kwargs['exc_info']

        if hasattr(err, "status_code"):
            status_code = err.status_code
            reason = err.reason
        else:
            status_code = 500
            reason = str(err)
        self.set_status(err.status_code)

        self.finish({
            'error': {
                'code': status_code,
                'message': reason,
            }
        })

    def write_json(self, response):
        self.write(json.dumps(response))

    def get_uid_channel(self):
        uid = self.get_query_argument("uid", default=None)
        channel_id = self.get_query_argument("channel_id", default=None)
        if uid is None:
            self.write_error_message(400, "缺少参数uid")

        elif channel_id is None:
            self.write_error_message(400, "缺少参数channel_id")
        else:
            return uid, channel_id

    def write_error_message(self, status_code, reason):
        self.set_status(status_code)
        self.finish({
            'error': {
                'code': status_code,
                'message': reason,
            }
        })

    def get_json_body(self):
        try:
            data = json.loads(self.request.body)
        except:
            data = json.loads(urllib.unquote_plus(self.request.body))
        return data
