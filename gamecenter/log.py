import logging
import os
from logging import handlers

from gamecenter import cfg

FMT = u'%(asctime)s %(levelname)-8s [%(name)s] %(message)s'


def setup():
    logging.basicConfig(
        format=(FMT)
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


def add_rotating_file_handler(log, name):
    path = cfg.config().get("DEFAULT", 'job_log_dir')
    if not os.path.exists(path):
        os.mkdir(path)

    file_handler = handlers.RotatingFileHandler(
        os.path.join(path, name),
        mode='a',
        maxBytes=int(cfg.config().getint("DEFAULT", 'log_size')),
        backupCount=int(cfg.config().get("DEFAULT", 'log_num')),
        # if backupCount is 0, rollover not happend.
    )
    formatter = logging.Formatter(FMT)
    file_handler.setFormatter(formatter)
    log.addHandler(file_handler)
