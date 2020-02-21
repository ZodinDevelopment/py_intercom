import os
import pyaudio
import wave
import time

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

def play_audio(outfile):
    wf = wave.open(outfile, 'rb')
    p = pyaudio.PyAudio()

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True)

    print('Playing last capture !!!')
    data = wf.readframes(CHUNK)

    while data != '':
        stream.write(data)
        data = wf.readframes(CHUNK)
        if len(data) <= 0:
            break

    stream.stop_stream()
    stream.close()
    p.terminate()

    print('Finished playback!')
    time.sleep(3)
    sys.exit()


def main():
    duration = str(input('Enter the duration of the audio capture [ex. 30 s -or- 10 m] >> '))

    secs = int(duration)
    outfile = str(input('Enter name for output file [ex. audio.wav]'))

    p = pyaudio.PyAudio()

    stream = p.open(format=FORMAT,
                    channels=CHANNELS,
                    rate=RATE,
                    input=True,
                    frames_per_buffer=CHUNK)

    print('* recording now for {} seconds'.format(str(secs)))

    frames = []

    for i in range(0, int(RATE / CHUNK * secs)):
        data = stream.read(CHUNK)
        frames.append(data)

    print('@@@ Done Recording @@@')
    stream.stop_stream()
    stream.close()
    p.terminate
    print('Saving to wave file.')

    wf = wave.open(outfile, 'wb')
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.setframerate(RATE)
    wf.writeframes(b''.join(frames))
    wf.close()

    print('Finished!')

    play_prompt = str(input('Would you like to hear the capture now? [y/n]>> '))

    if play_prompt.lower() == 'y':
        play_audio(outfile)

    else:
        print('Okay, see ya later fam!')
        time.sleep(3)
        sys.exit()

if __name__ == "__main__":
    main()
