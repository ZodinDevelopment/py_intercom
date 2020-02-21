import pyaudio
import wave 
#import socket 
import time 

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SECS = 5

HEADERSIZE = 10


def play_msg():
    infile = str(input('Enter filename >>'))
    wf = wave.open(infile, 'rb')

    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
        if len(data) <= 0:
            break
    stream.stop_stream()
    stream.close()

    p.terminate()


if __name__ == "__main__":
    play_msg()


