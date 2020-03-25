# -*- coding: utf-8 -*-

import copy
import hashlib
import json
import logging

from tornado import gen
from tornado.httpclient import HTTPClient
from tornado.httpclient import HTTPError
from tornado.httpclient import HTTPRequest

LOG = logging.getLogger(__name__)

ERROR_MSG = {
    0: u"成功",
    -1: u"参数为空",
    -2: u"签名错误",
    -3: u"参数userId为空",
    -4: u"参数gameId为空",
    -5: u"参数time为空",
    -6: u"参数signture为空",
    -7: u"已经登陆,不能重复登录",
    -8: u"渠道号错误",
    -9: u"公司不存在",
    -10: u"游戏不存在"

}


class GameSdk(object):
    default_options = {
        "method": "POST",
        "headers": {
            "Content-Type": 'application/json',
            "Content-Encoding": 'utf-8'
        },
        "validate_cert": False,
        "connect_timeout": 20,
        "request_timeout": 60
    }

    def __init__(self):
        # self.secret_key = cfg.config().get('SDK', 'cp_game_key')
        self.secret_key = "pg@wowei#!QAZ@WSX"
        # self.host = cfg.config().get("SDK", "host")
        self.host = "http://fw.woweicm.com"
        self.http_client = HTTPClient()
        self.logger = LOG

    def sign_generate(self, data):
        raw_str = ""
        for value in data:
            if value is not None:
                if isinstance(value, (int, float, long)):
                    value = str(value)
                elif isinstance(value, unicode):
                    value = value.encode('utf8')
                elif isinstance(value, (dict, tuple, list, set)):
                    value = json.dumps(value, separators=(',', ':'))
                raw_str += value
        raw_str += str(self.secret_key)

        sign = hashlib.md5(raw_str).hexdigest()
        return sign

    @gen.coroutine
    def _fetch_request(self, api, req_body):

        fetch = copy.deepcopy(self.default_options)

        url = self.host + api
        body = json.dumps(req_body)

        fetch["body"] = body
        fetch["url"] = url

        raise gen.Return(HTTPRequest(**fetch))

    @gen.coroutine
    def fetch_response(self, api, req_body):

        try:
            request = yield self._fetch_request(api, req_body)
            response = yield gen.maybe_future(self.http_client.fetch(request))

        except HTTPError as e:
            self.logger.exception(e)
            raise gen.Return({"msg": ""})
        else:
            if response.code == 200:
                resp_json = json.loads(response.body)
                raise gen.Return(resp_json)
            else:
                raise gen.Return({"msg": ""})

    def user_login_out(self, uids, channel_id):
        api = "/api/loginout"

        if isinstance(uids, list):
            uids = ";".join(uids)

        sign_list = [uids, channel_id]
        req_body = {
            "data": {
                "uids": uids,
                "channelId": channel_id
            },
            "signature": self.sign_generate(sign_list)
        }
        return self.fetch_response(api, req_body)

    def get_games(self, position):
        api = "/api/getgames"

        sign_list = [position]
        req_body = {
            "data": {
                "position": position
            },
            "signature": self.sign_generate(sign_list)
        }

        return self.fetch_response(api, req_body)

    def get_user_info(self, uid, channel_id):
        api = "/api/getuserinfo"

        sign_list = [uid, channel_id]

        req_body = {
            "data": {
                "uid": uid,
                "channelId": channel_id
            },
            "signature": self.sign_generate(sign_list)
        }

        return self.fetch_response(api, req_body)

    def user_login(self, uid, name, channel_id, game_id, icon_url):
        api = "/api/login"

        sign_list = [icon_url, game_id, channel_id, name, uid]

        req_body = {
            "data": {
                "uid": uid,
                "name": name,
                "gameId": game_id,
                "channelId": channel_id,
                "iconUrl": icon_url,
            },
            "signature": self.sign_generate(sign_list)
        }
        return self.fetch_response(api, req_body)


sdk = GameSdk()
