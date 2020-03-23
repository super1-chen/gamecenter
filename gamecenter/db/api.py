#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'
import logging

from gamecenter.db import models
from gamecenter.db import base
from gamecenter import cfg
from gamecenter import exception as g_exce

LOG = logging.getLogger(__name__)

class JOIN_STATUS(object):
    join = 0 # 参加游戏的人
    view = 1 # 观看游戏的人

def get_session():
    maker = base.maker(cfg.config().get('DB', 'sql_connection'), False)
    return maker()

# user
def user_get_by_uid_channel(uid, channel):
    model = models.User

    sess = get_session()
    query = sess.query(model).filter_by(uid=uid, channel=channel)
    return query.one_or_none()

def find_user(uid, channel):
    user = user_get_by_uid_channel(uid, channel)
    if user is None:
        raise g_exce.GameHttpError(reason=u'用户%s不存在' % uid, status_code=400)

    return user


def user_logout_by_uid_channel(uid, channel):

    model = models.User

    sess = get_session()

    with sess.begin():
        sess.query(model).filterfind_by(uid=uid, channel=channel).delete()


# room
def room_get_by_id(room_id):
    sess = get_session()
    return sess.query(models.Room).filter_by(id=room_id).one_or_none()


def find_room(room_id):
    room = room_get_by_id(room_id)
    if room is None:
        raise g_exce.GameHttpError(reason=u'未找到房间%s' %room_id , status_code=400)
    return room


def room_create_by_game(game_id, uid, channel, people=2):
    # 包含了一步加入逻辑
    Game = models.Game
    A = models.UserRoomAssociation
    Room = models.Room

    user = find_user(uid, channel)
    sess = get_session()

    with sess.begin():
        g = sess.query(Game).filter_by(id=game_id).one_or_none()
        if g is None:
            g = Game()
            g.id = game_id
            sess.add(g)
            sess.flush()
        room = Room()

        room.game_id = g.id
        room.people = people

        sess.add(room)
        sess.flush()

        a = A(user_id=user.id, room_id=room.id)
        sess.add(a)
    return ""

def check_room_full(room_id):
    A = models.UserRoomAssociation
    room = find_room(room_id)
    room_people = room.people
    sess = get_session()
    joined_people = sess.query(A).filter(A.room_id==room_id).filter(A.status==0).count()
    return room_people < joined_people



def user_join_room(room_id,  uid, channel):

    user = find_user(uid, channel)
    room = find_room(room_id)
    if check_room_full(room_id):
        raise g_exce.GameHttpError(400, "当前房间人数已满无法加入")

    sess = get_session()
    with sess.begin():
        a = models.UserRoomAssociation()
        a.user_id = user.id
        a.room_id = room.id
        sess.add(a)



def start_game(room_id, uid, channel):
    user = find_user(uid, channel)
    room = find_room(room_id)

    LOG.info("start user by %s" % user.uid)

    sess = get_session()
    with sess.begin():
        r = sess.query(models.Room).filter_by(id=room.id).one()
        r.status = 1
        sess.add(r)
