#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from yoctopuce.yocto_api import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_humidity import *

url = "http://oktorok.local/api/job"
headers = {'X-Api-Key': '4C06032E7E0B49709C5FF042E477178C'}
ymeteo = 'oktorokMeteo'
yrelay = 'oktorokRelay'
yerrormsg = YRefParam()


def secondstotime(s):
    if s is not None:
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return '{0:02d}:{1:02d}:{2:02d}'.format(h, m, s)
    else:
        h = '--'
        m = '--'
        s = '--'
        return '{}:{}:{}'.format(h, m, s)


def getcompletion(c):
    if c is not None:
        completion = round(c, 2)
    else:
        completion = '--'
    return completion


def gettemperature(target):
    sensor = YTemperature.FindTemperature(target + '.temperature')
    if sensor.isOnline():
        return "{0:.1f}".format(sensor.get_currentValue())
    else:
        return 'NaN'


def gethumidity(target):
    sensor = YHumidity.FindHumidity(target + '.humidity')
    if sensor.isOnline():
        return "{0:.1f}".format(sensor.get_currentValue())
    else:
        return 'NaN'


if YAPI.RegisterHub("http://oktorok.local", yerrormsg) != YAPI.SUCCESS:
    sys.exit("init error" + yerrormsg.value)

try:
    data = requests.get(url, headers=headers)
    json_data = json.loads(data.text)
except requests.exceptions.RequestException as e:
    print e
    sys.exit(1)


print json_data['job']['file']['name']
print getcompletion(json_data['progress']['completion'])
print secondstotime(json_data['progress']['printTimeLeft'])
print secondstotime(json_data['progress']['printTime'])
print gettemperature(ymeteo)
print gethumidity(ymeteo)
