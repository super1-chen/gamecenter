#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-23

__author__ = 'Albert'

from gamecenter.api.base import BaseCorsHandler

class NotFoundHandler(BaseCorsHandler):
    def prepare(self):  # for all methods
        self.write_error_message(404, "not found")