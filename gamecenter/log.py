import os
from os import path
import logging
from logging import handlers

from gamecenter import cfg


def setup():
    logging.basicConfig(
        format=(u'%(asctime)s %(levelname)-8s [%(name)s] %(message)s')
    )
    root_logger = logging.getLogger()

    if cfg.config().getboolean("DEFAULT", 'debug'):
        root_logger.setLevel(logging.DEBUG)
    else:
        root_logger.setLevel(logging.INFO)

    for l in ['requests', 'raven', 'urllib3', 'sh']:
        log = logging.getLogger(l)
        log.setLevel(logging.WARN)

    for l in ['peewee', 'huey', 'PIL']:
        log = logging.getLogger(l)
        log.setLevel(logging.INFO)



class LoggerMix(object):
    """
    Subclass will automatic get a field name `self.log`.
    """

    def __init__(self):
        self.log = logging.getLogger(self.full_name)

    @property
    def full_name(self):
        return self.__module__ + '.' + self.__class__.__name__

    @property
    def log_name(self):
        return self.full_name + '.log'
