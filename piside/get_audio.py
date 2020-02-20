import pyaudio
import wave 
import socket 
import time 

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SECS = 5

HEADERSIZE = 10


def play_msg():
    wf = wave.open('msg.wav', 'rb')

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


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((socket.gethostname(), 2348))
    while True:
        full_msg = b''
        while True:
            msg = s.recv(16)
            if len(msg) <= 0:
                break
            full_msg += msg

        if len(full_msg) > 0:
            with open('msg.wav', 'wb') as f:
                f.write(full_msg)

            print('Received')
            play_msg()
            break
    main()

if __name__ == "__main__":
    main()


