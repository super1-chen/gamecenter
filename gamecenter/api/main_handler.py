#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'

from gamecenter.api.base import BaseCorsHandler

class MainHandler(BaseCorsHandler):
    def get(self):
        self.write({"status": "success"})

    def post(self):
        self.write({"status": "success"})