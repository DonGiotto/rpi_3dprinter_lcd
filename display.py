#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
from time import sleep, strftime

import RPi_I2C_driver

from yoctopuce.yocto_api import *
from yoctopuce.yocto_temperature import *
from yoctopuce.yocto_humidity import *
from yoctopuce.yocto_carbondioxide import *

url = "http://oktorok.local/api/job"
headers = {'X-Api-Key': '4C06032E7E0B49709C5FF042E477178C'}
ymeteo = 'oktorokMeteo'
yco2 = 'oktorokCO2'
yrelay = 'oktorokRelay'
yerrormsg = YRefParam()
mylcd = RPi_I2C_driver.lcd()
displaytime = True

fontdata = [
    # Clock icon
    [0x0, 0xe, 0x15, 0x17, 0x11, 0xe, 0x0, 0x0],
    # Temperature icon
    [0x4, 0xa, 0xa, 0xa, 0xa, 0x11, 0x11, 0xe],
    # Celsius icon
    [0x8, 0x14, 0x8, 0x7, 0x8, 0x8, 0x8, 0x7],
    # Drop icon
    [0x0, 0x4, 0xa, 0x11, 0x11, 0x11, 0xe, 0x0],
    # Check icon
    [0x0, 0x1, 0x3, 0x16, 0x1c, 0x8, 0x0, 0x0],
    # Creeper
    [0x0, 0x1b, 0x1b, 0x4, 0xe, 0xe, 0xa, 0x0],
    # CO
    [0x9, 0x12, 0x9, 0x12, 0x9, 0x12, 0x9, 0x12],
]


def secondstotime(s):
    if s is not None:
        m, s = divmod(s, 60)
        h, m = divmod(m, 60)
        return '{0:02d}:{1:02d}'.format(h, m)
    else:
        h = '--'
        m = '--'
        s = '--'
        return '{}:{}'.format(h, m)


def getcompletion(c):
    if c is not None:
        completion = round(c, 2)
    else:
        completion = '--'
    return completion


def getco2(target):
    sensor = YCarbonDioxide.FindCarbonDioxide(target + '.carbonDioxide')
    if sensor.isOnline():
        return "{0:.0f}".format(sensor.get_currentValue())


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


def getpercent(p):
    return '{0:03d}'.format(int(p))


if YAPI.RegisterHub("http://oktorok.local", yerrormsg) != YAPI.SUCCESS:
    sys.exit("init error" + yerrormsg.value)

mylcd.lcd_clear()
mylcd.lcd_load_custom_chars(fontdata)
mylcd.lcd_display_string("Chileo Printer", 1)

mylcd.lcd_display_string_pos(unichr(1), 2, 0)
mylcd.lcd_display_string_pos(unichr(3), 2, 7)
mylcd.lcd_display_string_pos(unichr(6), 2, 14)
mylcd.lcd_display_string_pos(unichr(0), 4, 0)
mylcd.lcd_display_string_pos(unichr(4), 4, 7)
mylcd.lcd_display_string_pos(unichr(5), 4, 15)


while True:
    date = strftime("%H:%M")

    try:
        data = requests.get(url, headers=headers)
        json_data = json.loads(data.text)
    except requests.exceptions.RequestException as e:
        print e
        sys.exit(1)

    try:
        mylcd.lcd_display_string_pos(date, 1, 15)
        mylcd.lcd_display_string_pos(gettemperature(ymeteo) + unichr(2), 2, 1)
        mylcd.lcd_display_string_pos(gethumidity(ymeteo) + "%", 2, 8)
        mylcd.lcd_display_string_pos(getco2(yco2), 2, 15)

        mylcd.lcd_display_string_pos(
            secondstotime(json_data['progress']['printTime']
                          ), 4, 1)
        mylcd.lcd_display_string_pos(
            secondstotime(json_data['progress']['printTimeLeft']
                          ), 4, 8)

        mylcd.lcd_display_string_pos(
            getpercent(json_data['progress']['completion']) + "%", 4, 16)

    except (KeyboardInterrupt, SystemExit):
        print('Interrupt received, stopping...')
    sleep(30)


print json_data['job']['file']['name']
