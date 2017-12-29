#!/usr/bin/env python
# -*- coding: utf-8 -*-

import requests
import json
import sys
import RPi_I2C_driver

url = "http://10.10.11.70/api/printer?exclude=temperature,sd"
headers = {'X-Api-Key': '4C06032E7E0B49709C5FF042E477178C'}
printstate = "/home/pi/rpi_3dprinter_lcd/.printstate"

f = open(printstate, "r")
value = f.read(1)
f.close()


try:
    data = requests.get(url, headers=headers)
    json_data = json.loads(data.text)
except requests.exceptions.RequestException as e:
    print e
    sys.exit(1)

if value == '1':
    if json_data['state']['flags']['printing'] is False:
        f = open(printstate, "w")
        f.write('0')
        f.close()
	mylcd = RPi_I2C_driver.lcd()
        mylcd.backlight(0)

elif value == '0':
    if json_data['state']['flags']['printing'] is True:
        f = open(printstate, "w")
        f.write('1')
        f.close()
