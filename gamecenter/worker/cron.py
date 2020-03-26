# -*- coding: utf-8 -*-
import logging
import os
import signal
import time

from crontab import CronTab

from gamecenter import cfg
from gamecenter.worker import base


class Cron(object):
    def __init__(self):
        self.tabfile = cfg.config().get("WORKER",'crontab_file')
        open(self.tabfile, 'a').close()  # ensure crontab file exist
        self.cron = CronTab(tabfile=self.tabfile)
        self._logger = logging.getLogger("game.cron")
        self._stop_flag_timeout = 5
        self.stop_flag = False
        self._received_signal = False

    def remove_all(self):
        self.cron.remove_all()

    def register_default(self):
        pass

    def register_periodics(self):
        self.register_default()
        command = 'root /home/game_venv/bin/game-manage run_job '
        for kind, jobs in base.my_async.tasks.items():
            if kind != 'periodic_task':
                continue

            for job in jobs:
                job_name = job.origin_func.__name__
                cron_job = self.cron.new(
                    command + job_name + " >> /home/game_logs/%s.log 2>&1" % job_name)
                # Both Huey task / periodic_task decorator's first position
                # argument is validate_datetime
                cron_job.setall(job.job_args[0].cron_format)

    def save(self):
        self.cron.write()

    def delete_cron(self):
        if os.path.exists(self.tabfile):
            self._logger.info("delete cron.tab %s" % self.tabfile)
            os.remove(self.tabfile)

    def start(self):
        # if use with huey only run start
        self.remove_all()
        self.register_periodics()
        self.save()

    def run(self):
        self.start()
        timeout = self._stop_flag_timeout
        self.register_signal()
        msg = "=================== start was contab ======================="
        self._logger.info(msg)
        while True:
            try:
                self._logger.info("crontab is running")
                time.sleep(timeout)
            except KeyboardInterrupt:
                self.stop()
            except:
                self._logger.exception('Error in consumer.')
                self.stop()
            else:
                if self._received_signal:
                    self.stop()

            if self.stop_flag:
                break

        self._logger.info('Exit exiting.')

    def stop(self):
        self.stop_flag = True
        self.delete_cron()
        self._logger.info('Shutting down')

    def register_signal(self):
        signal.signal(signal.SIGTERM, self._handle_signal)
        # signal.signal(signal.SIGKILL, self._handle_signal)

    def _handle_signal(self, sig_num, frame):
        self._logger.info('Received SIGTERM')
        self._received_signal = True


def delete_crontab():
    tabfile = cfg.config().get("WORKER", 'crontab_file')
    if os.path.exists(tabfile):
        os.remove(tabfile)
