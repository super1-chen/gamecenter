#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-26

__author__ = 'Albert'

from gamecenter import log
from gamecenter import worker
from gamecenter.cmd import utils


def main():
    utils.load_config()
    log.setup()
    # huey 和 cron 一起用
    # worker.reset_cron()
    # worker.start_run()
    # 只使用cron
    worker.run_cron()