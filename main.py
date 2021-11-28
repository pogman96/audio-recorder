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

    if folderName not in os.listdir():
        os.mkdir(folderName)

    p = pyaudio.PyAudio()

    device_id = 14
    device_info = p.get_device_info_by_index(device_id)
    channels = device_info["maxInputChannels"] if (
        device_info["maxOutputChannels"] < device_info["maxInputChannels"]) else device_info["maxOutputChannels"]

    p.terminate()

    startTime = time.time()
    listOfNums = []

    while True:
        try:
            record(num, device_info=device_info, bitrate=bitrate, chunk=chunk, channels=channels,
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

    print(
        f"Recorded for {(num-startingNum) * recordingLength} recordingLength")

    with open("config.json", "r+") as file:
        conf["count"] = num
        json.dump(conf, file)


if __name__ == "__main__":
    main()
