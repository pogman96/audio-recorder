# Audio Recorder
 Records Desktop Audio
 
 Uses pyaudio fork https://github.com/intxcc/pyaudio_portaudio Python 3.7
 
 Uses wave library https://pypi.org/project/Wave/
 
 Execute to find device id
 ```python
import pyaudio

p = pyaudio.PyAudio()

print ("Available devices")
for i in range(0, p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print (str(info["index"]) + ": \t %s \n \t %s \n" % (info["name"], p.get_host_api_info_by_index(info["hostApi"])["name"]))
```
