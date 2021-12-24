from main import main

import pyaudio
import json

p = pyaudio.PyAudio()

print ("Available devices")
for i in range(0, p.get_device_count()):
   info = p.get_device_info_by_index(i)
   print (str(info["index"]) + ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))

in1 = input("Device ID: ")

with open("config.json", "r") as f:
    data = json.load(f)
    data["deviceID"] = int(in1)

with open("config.json", "w") as f:
    json.dump(data, f)


main()
