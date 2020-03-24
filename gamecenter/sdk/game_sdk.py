# -*- coding: utf-8 -*-

import hashlib
import json
import logging

import requests

from gamecenter import cfg

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

    def __init__(self):
        self.secret_key = cfg.config().get('SDK', 'cp_game_key')

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

    def proxy_request(self, api, method="post", data=None,
                      json_data=None, params=None, timeout=60):
        host = cfg.config().get("SDK", "host")

        url = host + api

        msg = ""
        msg_fmt = "Server Error: %s"
        code = 500
        ret = None

        try:
            headers = {
                "Content-Type": 'application/json',
                "Content-Encoding": 'utf-8'
            }
            kwargs = {
                "headers": headers,
                "verify": False,
                "data": data,
                "json": json_data,
                "params": params,
                "timeout": timeout
            }
            resp = requests.request(method, url, **kwargs)
            status_code = resp.status_code
            resp_json = resp.json()

            if status_code != 200:
                code = status_code
                msg = msg_fmt % resp_json
            else:
                code = resp_json.get("code")
                msg = ERROR_MSG.get(code)
                ret = resp_json.get("data")

        except requests.RequestException as e:
            LOG.error(e)
            msg = msg_fmt % str(e)

        finally:
            return code, msg, ret

    def user_login_out(self, uids, channel_id):
        api = "/api/loginout"

        if isinstance(uids, list):
            uids = ";".join(uids)

        sign_list = [uids, channel_id]
        req_json = {
            "data": {
                "uids": uids,
                "channelId": channel_id
            },
            "signature": self.sign_generate(sign_list)
        }
        return self.proxy_request(api=api, data=req_json)

    def get_games(self, position):
        api = "/api/getgames"

        sign_list = [position]
        req_json = {
            "data": {
                "position": position
            },
            "signature": self.sign_generate(sign_list)
        }

        return self.proxy_request(api=api, data=req_json)

    def get_user_info(self, uid, channel_id):
        api = "/api/getuserinfo"

        sign_list = [uid, channel_id]

        req_json = {
            "data": {
                "uid": uid,
                "channelId": channel_id
            },
            "signature": self.sign_generate(sign_list)
        }

        return self.proxy_request(api=api, data=req_json)

    def user_login(self, uid, name, channel_id, game_id, icon_url):
        api = "/api/login"

        sign_list = [icon_url, game_id, channel_id, name, uid]

        req_json = {
            "data": {
                "uid": uid,
                "name": name,
                "gameId": game_id,
                "channelId": channel_id,
                "iconUrl": icon_url,
            },
            "signature": self.sign_generate(sign_list)
        }

        return self.proxy_request(api=api, data=req_json)
