import json
import hashlib

data = ["http://www.baidu.com/image/1.png", 2,11000001,"test_004", "00000004"]

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
raw_str += str("pg@wowei#!QAZ@WSX")
print raw_str
sign = hashlib.md5(raw_str).hexdigest()
print sign