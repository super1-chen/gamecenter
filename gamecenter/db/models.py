#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'
import logging

from sqlalchemy import Boolean
from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import VARCHAR
from sqlalchemy import UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref
from sqlalchemy.sql.expression import text

from gamecenter import utils as center_utils

BASE = declarative_base()
LOG = logging.getLogger(__name__)


class User(BASE):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('uid', 'channel',
                         name='uid_channel_uc_name'),
    )

    id = Column(Integer, primary_key=True)
    created_time = Column(DateTime, default=center_utils.now)
    uid = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    name = Column(VARCHAR(255), nullable=False, server_default=text("''"))
    channel = Column(VARCHAR(128), nullable=False, server_default=text("''"))
    icon = Column(VARCHAR(1024), nullable=False, server_default=text("''"))



class Game(BASE):
    __tablename__ = 'games'
    id = Column(Integer, primary_key=True)  # // 这边id可以自己生成
    created_time = Column(DateTime, default=center_utils.now)
    update_time = Column(DateTime, default=center_utils.now, onupdate=center_utils.now)
    rooms = relationship('Room', lazy='joined', backref="game")


class Room(BASE):
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True)
    create_time = Column(DateTime, default=center_utils.now)
    status = Column(Boolean, default=False)  # 0 等待 1 开始
    people = Column(Integer, default=0)
    game_id = Column(Integer, ForeignKey('games.id'))
    users = relationship("UserRoomAssociation")


class UserRoomAssociation(BASE):
    __tablename__ = 'user_room_association'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    room_id = Column(Integer, ForeignKey('rooms.id'), primary_key=True)
    status = Column(Integer, default=0)
    user = relationship("User")