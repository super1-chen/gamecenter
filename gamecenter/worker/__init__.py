# -*- coding: utf-8 -*-
"""
Asynchronous task which invoked by api. The pattern here is "send and forget",
so do not depend on the result of tasks.
"""
import logging

from gamecenter import utils as game_utils
from gamecenter.log import add_rotating_file_handler
from gamecenter.worker import base
from gamecenter.worker import cron
#  if not import periodic here, periodic jobs will be GG!!!!
from gamecenter.worker import periodic  # noqa

LOG = logging.getLogger(__name__)


def reset_cron():
    c = cron.Cron()
    c.remove_all()
    c.register_periodics()
    c.save()


def run_cron():
    # 如果只使用cron调用这个命令
    c = cron.Cron()
    c.run()


def get_jobs():
    objs = []

    for kind, jobs in base.my_async.tasks.items():
        for job in jobs:
            objs.append(job.origin_func)

    return objs


def pretty_print_jobs():
    """
    显示周期任务和其对应的7日健康情况
    :return:
    """
    from terminaltables import AsciiTable  # noqa

    base_index = ['#', 'task', 'module']

    data = [base_index]
    for index, j in enumerate(get_jobs(), 1):
        job_info = [
            index,
            j.__name__,
            j.__module__
        ]
        data.append(job_info)

    table = AsciiTable(data)
    print(table.table)


def run_job(jobname):
    for job in get_jobs():
        if jobname == job.__name__:
            add_rotating_file_handler(LOG, job.__name__)

            start, error = game_utils.now(), False
            info = {
                "module": job.__module__,
                "name": job.__name__,
            }
            LOG.info("Start running %(module)s %(name)s" % info)

            try:
                job()

            except Exception:
                LOG.exception("Running %(module)s %(name)s failed" % info)
                error = True

            time_elapse = game_utils.now() - start

            info = {
                "module": job.__module__,
                "name": job.__name__,
                "start": start.strftime("%Y-%m-%d %H:%M:%S"),
                "cost": time_elapse.total_seconds()
            }

            if not error:
                LOG.info(
                    "Finished %(module)s %(name)s cost:"
                    " %(cost)ss success" % info)
            else:
                LOG.error(
                    "Finished %(module)s %(name)s cost:"
                    " %(cost)ss failed" % info)
            break
    else:
        print('Job: %s not found' % jobname)
