#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'

from tornado.web import HTTPError

class GameException(Exception):
    pass

class NotFoundException(Exception):
    pass

class GameHttpError(HTTPError):
    pass


class GetConfigBeforeLoad(GameException):
    pass