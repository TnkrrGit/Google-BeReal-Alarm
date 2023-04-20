# Author: Jorick Bouw
# Date: 2023-04-19
# Description: BeReal Alarm with Google Home

### Imports BeReal ###

import yaml
import requests
import schedule
import time
from datetime import datetime, timedelta

### Imports Google Home ###

import pychromecast
import time
from cryptography.hazmat.bindings.openssl.binding import Binding

### Startup ###

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

bereal_time_history_api = cfg['bereal']['bereal_time_history_api']
region = cfg['bereal']['region']
timezone = cfg['bereal']['time_zone']
device_name = cfg['google']['device_name']
alarm_url = cfg['google']['alarm_url']
debug = cfg['debug']

# Debugging:
if debug == True:
    print(f"bereal_time_history_api: {bereal_time_history_api}")
    print(f"region: {region}")
    print(f"device_name: {device_name}")
    print(f"alarm_url: {alarm_url}")

### Google Home Variables ###

chromecast_name = device_name
chromecasts = pychromecast.get_chromecasts()
# Debugging:
if debug == True:
    print("\n\nChromeCasts List:\n\n", chromecasts, "\n\n")
cast = next(
    cc for cc in chromecasts if cc.device.friendly_name == chromecast_name)
# Debugging:
if debug == True:
    print("\n\nSelected ChromeCast Information:\n\n", cast, "\n\n")
mc = cast.media_controller

### Google Home Functions ###


def alarm():
    mc.play_media(alarm_url,
                  content_type="audio/mp3")
    mc.block_until_active()
    mc.play()

### BeReal Variables ###


# Replace with your API key found on https://bereal.devin.fun/
API_KEY = bereal_time_history_api
# Replace with your desired region found on https://bereal.devin.fun/
REGION = region
INTERVAL = 1  # Check the API every 1 seconds
BeRealShot = False  # BeRealShot statement is defaulted to False

### BeReal Functions ###


def NieuweDag():
    global BeRealShot
    BeRealShot = False
    print("Nieuwe dag en reset OneShot")


def get_latest_moment():
    url = f'https://bereal.devin.rest/v1/moments/latest?api_key={API_KEY}'
    response = requests.get(url)
    data = response.json()
    return data['regions'][REGION]['utc']


def trigger_alarm():
    global BeRealShot
    if BeRealShot == False:
        print("Alarm triggered! Bereal was on ", latest_moment_datetime)
        alarm()
        BeRealShot = True


schedule.every().day.at("00:00").do(NieuweDag)

while True:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    latest_moment_clean = get_latest_moment()
    latest_moment_datetime = datetime.strptime(
        latest_moment_clean, '%Y-%m-%d %H:%M:%S')
    dt_utc1 = latest_moment_datetime + timedelta(hours=timezone)
    latest_moment = dt_utc1.strftime('%Y-%m-%d %H:%M:%S')

    if current_time >= str(latest_moment_datetime):
        trigger_alarm()
        # Debugging:
        if debug == True:
            print(f"current_time: {current_time}")
            print(f"latest_moment: {latest_moment}")

    schedule.run_pending()
    time.sleep(INTERVAL)
