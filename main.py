# Author: Jorick Bouw
# Date: 2023-04-19
# Description: BeReal Alarm with Google Home

### Imports BeReal ###

import requests
import schedule
import time
from datetime import datetime

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
