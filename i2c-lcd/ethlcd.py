#! /usr/bin/env python

import drivers
import requests
import ethlcd_config
import sys
from requests.exceptions import HTTPError

from time import sleep
from datetime import datetime
from subprocess import check_output

def logger(message):
    print(str(datetime.now()) + " " + message) 

def get_request(apiUrl):
    logger("Fetching eth hash rate request")
    try:
        response = requests.get(apiUrl)
        response.raise_for_status()
        return response

    except:
        e = sys.exc_info()[0]
        logger(e)

def show_hash(response):
    try:
        jsonResponse = response.json()
        currentHash = (jsonResponse["data"]["currentStatistics"]["currentHashrate"] / 1000000)
        reportedHash = (jsonResponse["data"]["currentStatistics"]["reportedHashrate"] / 1000000)
        logger("Current  " + str(currentHash))
        logger("Reported " + str(reportedHash))
        display.lcd_display_string("Curr  " + str("{:06.2F}".format(currentHash)) + "MH/s", 1)
        display.lcd_display_string("Repd  " + str("{:06.2F}".format(reportedHash)) + "MH/s", 2)

    except:
        e = sys.exc_info()[0]
        logger(e)

def show_ip():
    try:
        IP = check_output(["hostname", "-I"]).split()[0]
        print("Write to display")
        while True:
            display.lcd_display_string(str(datetime.now().time()), 1)
            display.lcd_display_string(str(IP), 2)
            sleep(1)

    except:
        e = sys.exc_info()[0]
        logger(e)

# initialize display
display = drivers.Lcd()
# grab minerUrl from ethlcd_config.py
minerUrl = ethlcd_config.minerUrl
try:
    while True:
        show_hash(get_request(minerUrl))
        sleep(300)

except KeyboardInterrupt:
    # If there is a KeyboardInterrupt (when you press ctrl+c), exit the program and cleanup
    logger("Cleaning up!")
    display.lcd_clear()
