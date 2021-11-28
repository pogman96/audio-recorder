import pyaudio
import wave


def record(num, device_info: dict, bitrate: int, chunk: int, channels: int, folderName: str, recordingLength: int, sampleRate: int):
    p = pyaudio.PyAudio()
    stream = p.open(format=bitrate,
                    channels=channels,
                    rate=int(device_info["defaultSampleRate"]),
                    input=True,
                    frames_per_buffer=chunk,
                    input_device_index=device_info["index"],
                    as_loopback=True
                    )

    frames = []

    print(f"Recording in {num}.wav")

    for _ in range(0, int(sampleRate / chunk * recordingLength)):
        data = stream.read(chunk)
        frames.append(data)

    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished recording')

    with wave.open(f"{folderName}/{num}.wav", 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(p.get_sample_size(bitrate))
        wf.setframerate(sampleRate)
        wf.writeframes(b''.join(frames))
