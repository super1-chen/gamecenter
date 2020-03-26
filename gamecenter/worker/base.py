# -*- coding: utf-8 -*-

import logging
from collections import defaultdict
from collections import namedtuple
from functools import wraps

LOG = logging.getLogger(__name__)

JobInfo = namedtuple("JobInfo", "job_args job_kwargs origin_func")


class Async(object):
    """
    Place to hold async jobs before init Huey.

    The sync jobs will become async jobs only when init is called,
    otherwise, decorated function is same as origin sync function.


    Example usage:

    my_async = Async()

    @my_async.task()
    def partner_connect(partner_id):
        # lone time job here
        pass

    Except origin Huey parameter, you can add boolean keyword arg master_only:

    @my_async.periodic_task(master_only=True)
    def the_job_run_on_master_only(arg1, arg2):
        # lone time job here
        pass

    Note:

    Extend Async.supported if we need support more
    huey decorator.
    """

    instance = None
    supported = ('periodic_task')

    def __new__(cls, *args, **kwargs):
        if Async.instance:
            return Async.instance

        base = super(Async, cls).__new__(cls, *args, **kwargs)
        Async.instance = base
        return base

    def __init__(self):
        self.tasks = defaultdict(list)
        self.async_func_map = {}

    def __getattr__(self, name):
        def add_task(*job_args, **job_kwargs):

            def func_wrapper(func):

                self.tasks[name].append(JobInfo(job_args, job_kwargs, func))

                @wraps(func)
                def async_func_wrapper(*args, **kwargs):
                    try:
                        async_func = self.async_func_map[func]

                    except KeyError:
                        LOG.warning("You need call was.worker.base.init"
                                    " if this is not unit test environment")

                        return func(*args, **kwargs)

                    return async_func(*args, **kwargs)

                return async_func_wrapper

            return func_wrapper

        if name in Async.supported:
            return add_task
        else:
            raise AttributeError


my_async = Async()


class A():
    pass


def crontab(month='*', day='*', day_of_week='*', hour='*', minute='*'):
    ret = A()
    ret.cron_format = ' '.join((minute, hour, day_of_week, day, month))
    return ret


def init():
    """
    Init Huey according to configuration and change decorated function
    to async jobs.
    """
    for task_kind, tasks in my_async.tasks.items():
        for task in tasks:
            my_async.async_func_map[task.origin_func] = task.origin_func
