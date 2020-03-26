#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'

import logging
from os import path as os_path

import configparser

from gamecenter import exception

LOG = logging.getLogger(__name__)
_load = False
_CFG = configparser.ConfigParser(allow_no_value=True)


def _get_etc_dir():
    """The root directory of xedge, such as `/home/gamecenter/etc`"""
    return os_path.join(os_path.dirname(os_path.abspath(__file__)),
                        os_path.pardir, 'etc')


def load_config(path=None, default=False):
    '''
    Optional function for load config file in specific path.

    This function is usually called in first place i.e. before any
    one calling config()
    '''
    global _load
    if not default:
        path = path or os_path.join(_get_etc_dir(), 'gamecenter.conf')
        _CFG.read(path)
    _load = True


def config():
    """Get an section from configuration"""
    global _load
    if _load:
        return _CFG
    else:
        raise exception.GetConfigBeforeLoad


def register(section, name, value, comment=None):
    """
    All default configuration must be declared here before using it.
    """
    if section != 'DEFAULT' and not _CFG.has_section(section):
        _CFG.add_section(section)

    if comment:
        _CFG.set(section, '# %s' % comment)
    _CFG.set(section, name, value)


def dump_example_config():
    path = os_path.join(_get_etc_dir(), 'gamecenter.conf.sample')
    with open(path, 'w') as configfile:
        _CFG.write(configfile)
    LOG.info("Dump to file: %s successfully." % path)

# default
register('DEFAULT', 'debug', 'true', comment='whether enable debug logging')
register('DEFAULT', 'log_size', '1048576', comment='log size, unit: Byte default 10MB')
register('DEFAULT', 'job_log_dir', '/home/gamecenter/game_logs', comment='job log dirname')
register('DEFAULT', 'log_num', '10', comment='log file number')

# mysql
register('DB', 'sql_connection', "mysql://root:123456@localhost/gamecenter",
         comment='Datebase url that xedge itself maintained')

# Mongodb part
register('MONGODB', 'mongodb_url', "mongodb://127.0.0.1:27017", comment='mongo address')


# SDK
register('SDK', 'cp_game_key', "xxxx", comment='SDK keys')
register('SDK', 'host', "xxxx", comment='SKD host')

# WORKER
register('WORKER', 'crontab_file', "/etc/cron.d/game.tab",
         comment="the gamecenter app own crontab file path")


# DELETE OLD DATA
register('OLD_DATA', 'keep_hour', "6", comment="old data key hours")