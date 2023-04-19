# Author: Jorick Bouw
# Date: 2023-04-19
# Description: BeReal Alarm with Google Home

### Imports BeReal ###

import requests
import schedule
import time
from datetime import datetime

### Imports Google Home ###

import pychromecast
import time
from cryptography.hazmat.bindings.openssl.binding import Binding

### Startup ###

### Google Home Variables ###

chromecast_name = "all"
chromecasts = pychromecast.get_chromecasts()
print(chromecasts)
cast = next(
    cc for cc in chromecasts if cc.device.friendly_name == chromecast_name)
print(cast)
mc = cast.media_controller

### Google Home Functions ###


def alarm():
    mc.play_media("https://dx35vtwkllhj9.cloudfront.net/universalstudios/super-mario-bros-plumbing/images/soundbites/completion-audio.mp3",
                  content_type="audio/mp3")
    mc.block_until_active()
    mc.play()

### BeReal Variables ###


# Replace with your API key found on https://bereal.devin.fun/
# Replace with your desired region found on https://bereal.devin.fun/
REGION = 'europe-west'
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
        print("Alarm triggered!")
        alarm()
        BeRealShot = True


schedule.every().day.at("00:00").do(NieuweDag)

while True:
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    latest_moment = get_latest_moment()
    latest_moment_datetime = datetime.strptime(
        latest_moment, '%Y-%m-%d %H:%M:%S')

    if current_time >= str(latest_moment_datetime):
        trigger_alarm()

    schedule.run_pending()
    time.sleep(INTERVAL)
