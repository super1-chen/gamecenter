#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'
import argparse
import datetime
import hashlib
import os

from gamecenter import cfg


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='use specific config file')
    args = parser.parse_args()

    if args.config:
        cfg.load_config(args.config)
    else:
        cfg.load_config()


def now(delay=None):
    """
    :para delay: `timedelta` object, if given, return datetime will delay
    by this timedelta.
    """
    n = datetime.datetime.now()
    if delay:
        n = n - delay
    return n


def format_time(datetime):
    TIME_FORAMT = '%Y-%m-%d %H:%M:%S'
    return datetime.strftime(TIME_FORAMT)


def md5(string):
    return hashlib.md5(string).hexdigest()


class TestingEnv(object):
    """
    Create a testing environment.

    Set OS environment variable WAS_TESTING, and recovery it
    to origin when exit.

    """

    def __enter__(self):
        self.origin_is_testing = bool(os.environ.get('WAS_TESTING'))
        os.environ["WAS_TESTING"] = '1'

    def __exit__(self, *exc):
        if not self.origin_is_testing:
            os.environ.pop("WAS_TESTING")
