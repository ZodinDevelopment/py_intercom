import pyaudio
import wave 
import socket
import time

HEADERSIZE = 10
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100
SECS = 5


def record():
    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print('* recording now')

    frames = []

    for i in range(0, int(RATE / CHUNK * SECS)):
        data = stream.read(CHUNK)
        frames.append(data)

    print('* Done recording')

    stream.stop_stream()
    stream.close()
    p.terminate

    wf = wave.open('data.wav', 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    with open('data.wav', 'rb') as f:
        data = f.read()

    return data 
    
def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((socket.gethostname(), 2348))
    s.listen(5)

    while True:
        clientsocket, address = s.accept()

        input('Press enter to send data')

        wf = record()
        print("Sending to clientside")
        
            

        clientsocket.send(wf)
        clientsocket.close()
        print("Success")
        
        
if __name__ == "__main__":
    main()

