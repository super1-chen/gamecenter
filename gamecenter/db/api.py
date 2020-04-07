#! /usr/bin/env python
# -*- coding: utf-8 -*-
# Create by Albert_Chen
# CopyRight (py) 2020年 陈超. All rights reserved by Chao.Chen.
# Create on 2020-03-22

__author__ = 'Albert'

import logging
import time

from gamecenter import cfg
from gamecenter import exception as g_exce
from gamecenter.db import base
from gamecenter.db import models

from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

LOG = logging.getLogger(__name__)


class ErrorMessage(object):
    user_join_error = u"用户在其他房间中不能重复加入"
    room_full_error = u"当前房间人数已满无法加入"
    room_start_error = u"当前房间游戏已经开始无法加入"
    user_no_found = u"用户%s不存在"
    room_no_found = u"房间%s不存在"
    user_no_in_room = u"用户%s不在房间%s中"
    game_start_error = u"房间%s已经开始游戏"
    room_no_empyt = u"房间中%s还有用户无法删除"


class JOIN_STATUS(object):
    join = 0  # 参加游戏的人
    view = 1  # 观看游戏的人


def get_session():
    maker = base.maker(cfg.config().get('DB', 'sql_connection'), False)
    return maker()


# user
def user_get_by_uid_channel(uid, channel):
    model = models.User

    sess = get_session()
    query = sess.query(model).filter_by(uid=uid, channel=channel)
    return query.one_or_none()


def user_create(**kwargs):
    channel = kwargs.get("channel_id")
    uid = kwargs.get("uid")
    insanity_dict = {
        "uid": uid,
        "icon": kwargs.get("icon"),
        "channel": channel,
        "name": kwargs.get("name")
    }

    sess = get_session()
    with sess.begin():
        user = sess.query(models.User).filter_by(uid=uid, channel=channel).one_or_none()
        if user is None:
            user = models.User()
        for k, v in insanity_dict.items():
            setattr(user, k, v)
        sess.add(user)
    return user

def user_delete(uid, channel):
    model = models.User
    sess = get_session()
    with sess.begin():
        sess.query(model).filter_by(uid=uid, channel=channel).delete()


def find_user(uid, channel):
    user = user_get_by_uid_channel(uid, channel)
    if user is None:
        raise g_exce.GameHttpError(reason=ErrorMessage.user_no_found % uid, status_code=400)

    return user


def user_logout_by_uid_channel(uid, channel):
    model = models.User

    sess = get_session()

    with sess.begin():
        sess.query(model).filterfind_by(uid=uid, channel=channel).delete()


# room
def room_list_get_game_id(game_id):
    sess = get_session()
    records = sess.query(models.Room).options(joinedload(models.Room.users)).filter(
        models.Room.game_id == game_id).all()
    return records


def room_get_by_id(room_id):
    sess = get_session()
    return sess.query(models.Room).options(joinedload(models.Room.users)).filter_by(id=room_id).one_or_none()


def find_room(room_id):
    room = room_get_by_id(room_id)
    if room is None:
        raise g_exce.GameHttpError(reason=ErrorMessage.room_no_found % room_id, status_code=400)

    return room


def room_create_by_game(game_id, uid, channel, people=2):
    # 包含了一步加入逻辑
    Game = models.Game
    User = models.User
    Room = models.Room

    user = find_user(uid, channel)
    sess = get_session()

    if user_joined_room(user.id):
        raise g_exce.HTTPError(reason=ErrorMessage.user_join_error, status_code=400)

    with sess.begin():

        g = sess.query(Game).filter_by(id=game_id).one_or_none()
        u = sess.query(User).filter_by(id=user.id).one_or_none()
        if g is None:
            g = Game()
            g.id = game_id
            sess.add(g)
            sess.flush()
        room = Room()

        room.game_id = g.id
        room.people = people
        a = models.UserRoomAssociation(user_id=user.id, room_id=room.id)
        room.users.append(a)
        sess.add(room)
    return room


def user_joined_room(user_id):
    """
    user表中的id
    :param user_id:
    :return:
    """
    sess = get_session()
    return sess.query(models.UserRoomAssociation).filter(models.UserRoomAssociation.user_id == user_id).count() > 0


def user_in_room(user_id, room_id):
    Associaton = models.UserRoomAssociation
    sess = get_session()
    return sess.query(Associaton).filter_by(user_id=user_id, room_id=room_id).count() > 0


def check_room_full(room_id):
    A = models.UserRoomAssociation
    room = find_room(room_id)
    room_people = room.people
    sess = get_session()
    joined_people = sess.query(A).filter(A.room_id == room_id).filter(A.status == 0).count()
    return room_people < joined_people


def user_join_room(room_id, uid, channel):
    user = find_user(uid, channel)
    room = find_room(room_id)

    if room.status:
        raise g_exce.GameHttpError(reason=ErrorMessage.room_start_error, status_code=400)
    if check_room_full(room_id):
        raise g_exce.GameHttpError(reason=ErrorMessage.room_full_error, status_code=400)
    if user_joined_room(user_id=user.id):
        raise g_exce.GameHttpError(reason=ErrorMessage.user_join_error, status_code=400)

    sess = get_session()
    with sess.begin():
        a = models.UserRoomAssociation()
        a.user_id = user.id
        a.room_id = room.id
        sess.add(a)


def user_quite_room(uid, channel_id):
    user = find_user(uid, channel_id)
    model = models.UserRoomAssociation

    sess = get_session()
    sess.query(model).filter(model.user_id == user.id).delete()


def delete_empty_room(uid, channel_id):
    user = find_user(uid, channel_id)
    model = models.UserRoomAssociation

    sess = get_session()
    with sess.begin():
        a = sess.query(model).filter(model.user_id == user.id).one_or_none()
        room_id = a.room_id
        delete_flag = False
        if a is not None:
            a_other = sess.query(model).filter(model.room_id == a.room_id, model.user_id != user.id).all()
            if a_other == 0:
                delete_flag = True
            sess.delete(a)
            sess.flush()
        if delete_flag is True:
            sess.query(models.Room).filter(models.Room.id == room_id).delete()


def delete_room(uid, channel_id, room_id):
    model = models.Room
    sess = get_session()
    with sess.begin():
        try:
            sess.query(model).filter(model.id == room_id).delete()
        except IntegrityError:
            raise g_exce.HTTPError(status_code=400, reason=ErrorMessage.room_no_empyt % room_id)


def start_game(uid, channel, room_id):

    user = find_user(uid, channel)
    room = find_room(room_id)
    if not user_in_room(user.id, room.id):
        raise g_exce.HTTPError(status_code=400, reason=ErrorMessage.user_no_in_room % (uid, room_id))
    if room.status:
        raise g_exce.HTTPError(status_code=400, reason=ErrorMessage.game_start_error % room_id)

    LOG.info("start user by %s" % user.uid)

    sess = get_session()
    with sess.begin():
        r = sess.query(models.Room).filter_by(id=room.id).one()
        r.status = True
        r.start_time = int(time.time())
        sess.add(r)


def end_game(uid, channel, room_id):
    user = find_user(uid, channel)
    room = find_room(room_id)
    if not user_in_room(user.id, room.id):
        raise g_exce.HTTPError(status_code=400, reason=ErrorMessage.user_no_in_room % (uid, room_id))

    LOG.info("stop user by %s" % user.uid)

    sess = get_session()

    with sess.begin():
        r = sess.query(models.Room).filter_by(id=room.id).one()
        r.status = False
        r.start_time = int(time.time())
        sess.add(r)
