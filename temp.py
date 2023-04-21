import yaml

with open("config.yml", "r") as ymlfile:
    cfg = yaml.load(ymlfile, Loader=yaml.SafeLoader)

bereal_time_history_api = cfg['bereal']['bereal_time_history_api']
region = cfg['bereal']['region']
device_name = cfg['google']['device_name']
alarm_url = cfg['google']['alarm_url']

print(f"bereal_time_history_api: {bereal_time_history_api}")
print(f"region: {region}")
print(f"device_name: {device_name}")
print(f"alarm_url: {alarm_url}")

# import pychromecast
# import time
# from cryptography.hazmat.bindings.openssl.binding import Binding

# chromecast_name = "Slaapkamer"
# chromecasts = pychromecast.get_chromecasts()
# print(chromecasts)
# cast = next(
#     cc for cc in chromecasts if cc.device.friendly_name == chromecast_name)
# print(type(cast))
# mc = cast.media_controller


# def alarm():
#     mc.play_media("https://dx35vtwkllhj9.cloudfront.net/universalstudios/super-mario-bros-plumbing/images/soundbites/completion-audio.mp3",
#                   content_type="mpeg/mp3")
#     mc.block_until_active()
#     mc.play()


# print("Alarm is gestart")
# alarm()
# time.sleep(20)
# print("En NU NOGEENS")
# alarm()
