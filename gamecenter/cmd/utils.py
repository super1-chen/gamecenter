# -*- coding: utf-8 -*-
import argparse

from gamecenter import cfg


def load_config():
    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config', help='use specific config file')
    args = parser.parse_args()

    if args.config:
        cfg.load_config(args.config)
    else:
        cfg.load_config()
