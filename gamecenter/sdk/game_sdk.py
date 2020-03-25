# -*- coding: utf-8 -*-

import copy
import hashlib
import json
import logging

import requests
from tornado.web import HTTPError

ERROR_MSG = {
    0: "success",
    -1: "empty params error",
    -2: "missing signature",
    -3: "missing key words userId",
    -4: "missing key words gameId",
    -5: "missing key words time",
    -6: "signature error",
    -7: "user logged error",
    -8: "wrong channel error",
    -9: "company not exist",
    -10: "game not exist",
    -99: "unknown error"
}

ERROR_MSG_ALIAS = {
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
    -10: u"游戏不存在",
    -99: u"未知错误"
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

    def __init__(self, host, security_key):
        self.secret_key = security_key
        self.host = host
        self.logger = logging.getLogger("game sdk")

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

    def _fetch_request(self, api, req_body):

        fetch = copy.deepcopy(self.default_options)

        url = self.host + api
        body = json.dumps(req_body)

        fetch["body"] = body
        fetch["url"] = url

        return requests.post(url, json=req_body, timeout=600)

    def fetch_response(self, api, req_body):
        try:
            self.logger.info("post api %s body %s" %(api, req_body))
            resp = self._fetch_request(api, req_body)
        except requests.Timeout as e:
            self.logger.error(e)
            status_code = 500
            reason = 'sdk响应超时'
            raise HTTPError(status_code=status_code, reason=reason)
        else:
            if resp.status_code == 200:
                resp_json = resp.json()
                code = int(resp_json.get("code", -99))

                if int(code) == 0:
                    self.logger.info("get sdk %s success %s" % (api, resp_json))
                    return resp_json
                else:
                    error_message = ERROR_MSG.get(code, ERROR_MSG.get(-99))
                    error_message_alias = ERROR_MSG_ALIAS.get(code, ERROR_MSG_ALIAS.get(-99))
                    self.logger.error("get skd %s failed by %s" % (api, error_message))
                    raise HTTPError(status_code=400, reason=error_message_alias)

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

    def get_games(self, position="1"):
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


SDK_CACHE = {}


def create_sdk(host, secret_key):
    key = hashlib.md5(host + secret_key).hexdigest()
    if key in SDK_CACHE and SDK_CACHE.get(key) is not None:
        sdk = SDK_CACHE.get(key)
    else:
        sdk = GameSdk(host, secret_key)
        SDK_CACHE[key] = sdk
    return sdk
