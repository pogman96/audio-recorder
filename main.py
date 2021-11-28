import pyaudio
import json
import time
import os
from record import record


def main():

    with open("config.json", "r") as file:
        conf = json.load(file)
        startingNum = conf["count"]
        num = conf["count"]
        chunk = conf["chunk"]
        bitrate = eval(f"pyaudio.paInt{conf['bitrate']}")
        channels = conf["channels"]
        sampleRate = conf["sampleRate"]
        recordingLength = conf["recordingLength"]
        deletionQuota = conf["deletionQuota"]
        folderName = conf["folderName"]
        deviceID = conf["deviceID"]

    if folderName not in os.listdir():
        os.mkdir(folderName)

    p = pyaudio.PyAudio()
    deviceInfo = p.get_device_info_by_index(deviceID)
    channels = deviceInfo["maxInputChannels"] if (deviceInfo["maxOutputChannels"] < deviceInfo["maxInputChannels"]) else deviceInfo["maxOutputChannels"]
    p.terminate()

    startTime = time.time()
    listOfNums = []

    while True:
        try:
            record(num, deviceInfo=deviceInfo, bitrate=bitrate, chunk=chunk, channels=channels,
                   folderName=folderName, recordingLength=recordingLength, sampleRate=sampleRate)
            listOfNums.append(num)
            elap = time.time() - startTime
            print(elap)
            if elap >= deletionQuota:
                for i in range(deletionQuota//recordingLength):
                    os.remove(f"{folderName}/{listOfNums[i]}.wav")
                listOfNums = listOfNums[deletionQuota//recordingLength:]
                startTime = time.time()
            num += 1

        except KeyboardInterrupt:
            print("Exiting")
            break

    print(f"Recorded for {(num-startingNum) * recordingLength} seconds")

    with open("config.json", "r+") as file:
        conf["count"] = num
        json.dump(conf, file)


if __name__ == "__main__":
    main()
